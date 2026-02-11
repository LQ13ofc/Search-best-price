import flet as ft
import httpx
import asyncio
import json
import os
import csv
import shutil
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import threading
import time

DATA_FILE = "data.json"
CACHE_FILE = "cache.json"
CONFIG_FILE = "config.json"
CACHE_TTL = 3600
CHECK_INTERVAL = 1800

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"AVISO: {CONFIG_FILE} corrompido. Usando padrões.")
            return {"serpapi_key": os.getenv("SERPAPI_KEY", "")}
        except Exception as e:
            print(f"Erro ao carregar config: {e}")
            return {"serpapi_key": os.getenv("SERPAPI_KEY", "")}
    return {"serpapi_key": os.getenv("SERPAPI_KEY", "")}

def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar config: {e}")

config = load_config()
SERPAPI_KEY = config.get("serpapi_key", "")

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"AVISO: Arquivo {DATA_FILE} corrompido. Fazendo backup...")
            backup_file = f"{DATA_FILE}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            try:
                import shutil
                shutil.copy(DATA_FILE, backup_file)
                print(f"Backup salvo em: {backup_file}")
            except:
                pass
            return {"history": [], "favorites": [], "price_history": {}, "alerts": []}
        except Exception as e:
            print(f"Erro ao carregar {DATA_FILE}: {e}")
            return {"history": [], "favorites": [], "price_history": {}, "alerts": []}
    return {"history": [], "favorites": [], "price_history": {}, "alerts": []}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"AVISO: Cache corrompido. Limpando...")
            return {}
        except Exception as e:
            print(f"Erro ao carregar cache: {e}")
            return {}
    return {}

def save_cache(cache):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except:
        pass

data = load_data()
cache = load_cache()

def get_from_cache(query: str, filters: dict) -> Optional[List[Dict]]:
    cache_key = f"{query}_{json.dumps(filters, sort_keys=True)}"
    if cache_key in cache:
        entry = cache[cache_key]
        timestamp = datetime.fromisoformat(entry["timestamp"])
        if datetime.now() - timestamp < timedelta(seconds=CACHE_TTL):
            return entry["data"]
    return None

def save_to_cache(query: str, filters: dict, data_list: List[Dict]):
    cache_key = f"{query}_{json.dumps(filters, sort_keys=True)}"
    cache[cache_key] = {
        "timestamp": datetime.now().isoformat(),
        "data": data_list
    }
    save_cache(cache)

def add_price_to_history(product_id: str, price: float, loja: str):
    if product_id not in data["price_history"]:
        data["price_history"][product_id] = []
    
    data["price_history"][product_id].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "price": price,
        "loja": loja
    })
    
    if len(data["price_history"][product_id]) > 30:
        data["price_history"][product_id] = data["price_history"][product_id][-30:]
    
    save_data(data)

def get_price_history(product_id: str) -> List[Dict]:
    return data["price_history"].get(product_id, [])

def get_lowest_price(product_id: str) -> Optional[float]:
    history = get_price_history(product_id)
    if history:
        return min(h["price"] for h in history)
    return None

def check_price_alerts(notification_callback):
    while True:
        try:
            for fav in data["favorites"]:
                product_id = fav.get("id")
                if not product_id:
                    continue
                
                alert = next((a for a in data["alerts"] if a["product_id"] == product_id and a["enabled"]), None)
                if not alert:
                    continue
                
                current_price = fav.get("preco")
                threshold = alert["threshold_price"]
                
                if current_price and current_price <= threshold:
                    notification_callback(f"🎉 ALERTA! {fav['titulo'][:50]} está R$ {current_price:.2f} (abaixo de R$ {threshold:.2f})")
        except Exception as e:
            print(f"Erro no check de alertas: {e}")
        
        time.sleep(CHECK_INTERVAL)

async def buscar_mercado_livre(query: str, max_price: Optional[float] = None) -> List[Dict]:
    try:
        url = "https://api.mercadolibre.com/sites/MLB/search"
        params = {
            "q": query.replace(" ", "+"),
            "sort": "price_asc",
            "limit": 50,
            "condition": "new"
        }
        
        async with httpx.AsyncClient(timeout=12) as client:
            r = await client.get(url, params=params)
            items = r.json().get("results", [])
        
        results = []
        for item in items:
            price = item.get("price")
            if not price or (max_price and price > max_price):
                continue
            
            product_id = item.get("id")
            results.append({
                "id": product_id,
                "loja": "Mercado Livre",
                "titulo": item["title"][:110],
                "preco": price,
                "link": item["permalink"],
                "imagem": item.get("thumbnail"),
                "source": "ml",
                "frete_gratis": item.get("shipping", {}).get("free_shipping", False),
                "vendedor": item.get("seller", {}).get("nickname", "N/A")
            })
            
            add_price_to_history(product_id, price, "Mercado Livre")
        
        return results
    except Exception as e:
        print(f"Erro ML: {e}")
        return []

async def buscar_google_shopping(query: str, max_price: Optional[float] = None, api_key: str = "") -> List[Dict]:
    if not api_key:
        return []
    try:
        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google_shopping",
            "q": query,
            "gl": "br",
            "hl": "pt",
            "api_key": api_key,
            "num": 30
        }
        
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url, params=params)
            items = r.json().get("shopping_results", [])
        
        results = []
        for item in items:
            price = item.get("extracted_price") or item.get("price")
            if isinstance(price, str):
                try:
                    price_clean = price.replace("R$", "").replace(" ", "").strip()
                    price_clean = price_clean.replace(".", "").replace(",", ".")
                    price = float(price_clean)
                except:
                    continue
            
            if not isinstance(price, (int, float)) or price <= 0:
                continue
            
            if max_price and price > max_price:
                continue
            
            product_id = str(item.get("product_id") or hash(item.get("link")))
            results.append({
                "id": product_id,
                "loja": item.get("source", "Google Shopping"),
                "titulo": item.get("title", "")[:110],
                "preco": float(price),
                "link": item.get("link"),
                "imagem": item.get("thumbnail"),
                "source": "shopping",
                "frete_gratis": False,
                "vendedor": item.get("source", "N/A")
            })
            
            add_price_to_history(product_id, price, item.get("source", "Google Shopping"))
        
        return results
    except Exception as e:
        print(f"Erro Google Shopping: {e}")
        return []

def main(page: ft.Page):
    page.title = "Caçador de Preços"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 1200
    page.window_height = 800
    
    current_results = []
    notifications_list = []
    
    def show_notification(message: str):
        def _show():
            notifications_list.insert(0, {"message": message, "time": datetime.now().strftime("%H:%M")})
            if len(notifications_list) > 10:
                notifications_list.pop()
            page.show_snack_bar(ft.SnackBar(
                content=ft.Text(message, size=16),
                bgcolor=ft.colors.GREEN_700,
                duration=5000
            ))
        
        try:
            page.run_task(_show)
        except:
            print(f"Notificação: {message}")
    
    alert_thread = threading.Thread(target=check_price_alerts, args=(show_notification,), daemon=True)
    alert_thread.start()
    
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=True,
        tabs=[
            ft.Tab(text="Buscar", icon=ft.icons.SEARCH),
            ft.Tab(text="Histórico", icon=ft.icons.HISTORY),
            ft.Tab(text="Favoritos", icon=ft.icons.FAVORITE),
            ft.Tab(text="Gráficos", icon=ft.icons.ANALYTICS),
            ft.Tab(text="Alertas", icon=ft.icons.NOTIFICATIONS),
            ft.Tab(text="Configurações", icon=ft.icons.SETTINGS),
        ]
    )
    
    txt_busca = ft.TextField(
        label="Produto (ex: rtx 5060, iphone 15)",
        expand=True,
        autofocus=True,
        prefix_icon=ft.icons.SHOPPING_CART
    )
    txt_preco_max = ft.TextField(
        label="Preço máximo",
        width=140,
        suffix_text="R$",
        keyboard_type=ft.KeyboardType.NUMBER
    )
    ddl_ordem = ft.Dropdown(
        width=170,
        value="price_asc",
        options=[
            ft.dropdown.Option("price_asc", "💰 Menor preço"),
            ft.dropdown.Option("relevance", "⭐ Relevância")
        ]
    )
    
    chk_frete_gratis = ft.Checkbox(label="Frete grátis", value=False)
    ddl_loja = ft.Dropdown(
        width=180,
        value="todas",
        options=[
            ft.dropdown.Option("todas", "Todas as lojas"),
            ft.dropdown.Option("ml", "Mercado Livre"),
            ft.dropdown.Option("shopping", "Google Shopping")
        ]
    )
    
    loading = ft.ProgressRing(visible=False)
    status = ft.Text("")
    resultados_view = ft.ListView(expand=True, spacing=12, padding=15)
    
    async def buscar(e=None):
        nonlocal current_results
        query = txt_busca.value.strip()
        if not query:
            page.show_snack_bar(ft.SnackBar(ft.Text("Digite o produto")))
            return
        
        filters = {
            "max_price": txt_preco_max.value,
            "frete_gratis": chk_frete_gratis.value,
            "loja": ddl_loja.value
        }
        
        cached = get_from_cache(query, filters)
        if cached:
            current_results = cached
            resultados_view.controls.clear()
            for item in current_results[:80]:
                is_fav = any(f.get("id") == item.get("id") for f in data["favorites"])
                resultados_view.controls.append(criar_card(item, is_fav))
            status.value = f"✅ {len(cached)} produtos (cache)"
            page.update()
            return
        
        loading.visible = True
        status.value = "Buscando..."
        resultados_view.controls.clear()
        page.update()
        
        try:
            max_p = float(txt_preco_max.value.replace(",", ".")) if txt_preco_max.value.strip() else None
        except:
            max_p = None
        
        ml, shopping = await asyncio.gather(
            buscar_mercado_livre(query, max_p),
            buscar_google_shopping(query, max_p, config.get("serpapi_key", ""))
        )
        todos = ml + shopping
        
        if chk_frete_gratis.value:
            todos = [p for p in todos if p.get("frete_gratis")]
        
        if ddl_loja.value != "todas":
            todos = [p for p in todos if p.get("source") == ddl_loja.value]
        
        if ddl_ordem.value == "price_asc":
            todos.sort(key=lambda x: x["preco"])
        
        current_results = todos
        save_to_cache(query, filters, todos)
        
        if query not in [h["query"] for h in data["history"]]:
            data["history"].insert(0, {
                "query": query,
                "date": datetime.now().strftime("%d/%m %H:%M"),
                "results": len(todos)
            })
            if len(data["history"]) > 50:
                data["history"].pop()
            save_data(data)
        
        resultados_view.controls.clear()
        for item in todos[:80]:
            is_fav = any(f.get("id") == item.get("id") for f in data["favorites"])
            resultados_view.controls.append(criar_card(item, is_fav))
        
        loading.visible = False
        status.value = f"✅ {len(todos)} produtos"
        page.update()
    
    def criar_card(item: Dict, is_fav: bool):
        product_id = item.get("id")
        lowest = get_lowest_price(product_id)
        is_lowest = lowest and item["preco"] <= lowest
        
        def fav_click(e):
            if is_fav:
                data["favorites"] = [f for f in data["favorites"] if f.get("id") != product_id]
            else:
                item_copy = item.copy()
                item_copy["saved_date"] = datetime.now().strftime("%d/%m/%Y")
                data["favorites"].append(item_copy)
            save_data(data)
            page.update()
        
        badges = []
        if item.get("frete_gratis"):
            badges.append(ft.Container(
                content=ft.Text("FRETE GRÁTIS", size=11, weight=ft.FontWeight.BOLD),
                bgcolor=ft.colors.GREEN_700,
                padding=5,
                border_radius=5
            ))
        if is_lowest:
            badges.append(ft.Container(
                content=ft.Text("MENOR PREÇO", size=11, weight=ft.FontWeight.BOLD),
                bgcolor=ft.colors.ORANGE_700,
                padding=5,
                border_radius=5
            ))
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Image(
                            src=item.get("imagem"),
                            width=80,
                            height=80,
                            fit=ft.ImageFit.CONTAIN
                        ) if item.get("imagem") else ft.Icon(ft.icons.SHOPPING_CART, size=60),
                        ft.Column([
                            ft.Text(item["titulo"], size=14, weight=ft.FontWeight.W_500, max_lines=2),
                            ft.Text(f"{item['loja']}", color=ft.colors.BLUE_400, size=12),
                            ft.Row(badges, spacing=5) if badges else ft.Container()
                        ], expand=True, spacing=4),
                        ft.IconButton(
                            icon=ft.icons.FAVORITE if is_fav else ft.icons.FAVORITE_BORDER,
                            icon_color=ft.colors.RED_400,
                            on_click=fav_click,
                            tooltip="Favoritar"
                        )
                    ], spacing=10),
                    ft.Divider(height=1),
                    ft.Row([
                        ft.Text(
                            f"R$ {item['preco']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.GREEN_400
                        ),
                        ft.ElevatedButton(
                            "Ver oferta",
                            icon=ft.icons.OPEN_IN_NEW,
                            on_click=lambda _, link=item["link"]: page.launch_url(link)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ], spacing=8),
                padding=14
            ),
            elevation=3
        )
    
    busca_tab = ft.Column([
        ft.Row([txt_busca, txt_preco_max, ddl_ordem], spacing=10),
        ft.Row([chk_frete_gratis, ddl_loja, ft.ElevatedButton("Buscar", on_click=buscar, style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE_700
        ))], spacing=10),
        ft.Row([loading, status]),
        resultados_view
    ], expand=True, spacing=12)
    
    historico_view = ft.ListView(expand=True, spacing=8, padding=15)
    
    def atualizar_historico():
        historico_view.controls.clear()
        for h in data["history"]:
            historico_view.controls.append(
                ft.Card(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.icons.SEARCH, color=ft.colors.BLUE_400),
                        title=ft.Text(h["query"], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"{h['date']} • {h.get('results', 0)} resultados"),
                        on_click=lambda e, q=h["query"]: (
                            setattr(txt_busca, 'value', q),
                            setattr(tabs, 'selected_index', 0),
                            page.update(),
                            asyncio.create_task(buscar())
                        ),
                        trailing=ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            on_click=lambda e, hh=h: (
                                data["history"].remove(hh),
                                save_data(data),
                                atualizar_historico()
                            )
                        )
                    )
                )
            )
        page.update()
    
    historico_tab = ft.Column([
        ft.Row([
            ft.Text("Histórico de Buscas", size=20, weight=ft.FontWeight.BOLD),
            ft.IconButton(
                icon=ft.icons.DELETE_SWEEP,
                tooltip="Limpar histórico",
                on_click=lambda e: (
                    data.__setitem__("history", []),
                    save_data(data),
                    atualizar_historico()
                )
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        historico_view
    ], expand=True)
    
    favoritos_view = ft.ListView(expand=True, spacing=12, padding=15)
    
    def atualizar_favoritos():
        favoritos_view.controls.clear()
        if not data["favorites"]:
            favoritos_view.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.FAVORITE_BORDER, size=80, color=ft.colors.GREY_500),
                        ft.Text("Nenhum favorito", size=18, color=ft.colors.GREY_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    expand=True
                )
            )
        else:
            for item in data["favorites"]:
                favoritos_view.controls.append(criar_card(item, True))
        page.update()
    
    favoritos_tab = ft.Column([
        ft.Row([
            ft.Text("Favoritos", size=20, weight=ft.FontWeight.BOLD),
            ft.IconButton(
                icon=ft.icons.REFRESH,
                tooltip="Atualizar",
                on_click=lambda e: atualizar_favoritos()
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        favoritos_view
    ], expand=True)
    
    graficos_view = ft.ListView(expand=True, spacing=15, padding=15)
    
    def atualizar_graficos():
        graficos_view.controls.clear()
        
        if not data["favorites"]:
            graficos_view.controls.append(
                ft.Container(
                    content=ft.Text("Adicione favoritos para ver análises", size=16),
                    alignment=ft.alignment.center,
                    expand=True
                )
            )
            page.update()
            return
        
        for fav in data["favorites"][:10]:
            product_id = fav.get("id")
            history = get_price_history(product_id)
            
            if len(history) < 2:
                continue
            
            dates = [h["date"][-5:] for h in history[-10:]]
            prices = [h["price"] for h in history[-10:]]
            
            lowest = min(prices)
            highest = max(prices)
            current = prices[-1]
            
            graficos_view.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(fav["titulo"][:80], size=16, weight=ft.FontWeight.BOLD),
                            ft.Row([
                                ft.Column([
                                    ft.Text("Atual", size=12, color=ft.colors.GREY_400),
                                    ft.Text(f"R$ {current:.2f}", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400)
                                ]),
                                ft.Column([
                                    ft.Text("Menor", size=12, color=ft.colors.GREY_400),
                                    ft.Text(f"R$ {lowest:.2f}", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_400)
                                ]),
                                ft.Column([
                                    ft.Text("Maior", size=12, color=ft.colors.GREY_400),
                                    ft.Text(f"R$ {highest:.2f}", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.RED_400)
                                ])
                            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Histórico:", size=12, color=ft.colors.GREY_400),
                                    ft.Row([
                                        ft.Text(f"{d}: R$ {p:.2f}", size=11)
                                        for d, p in zip(dates, prices)
                                    ], wrap=True)
                                ]),
                                padding=10,
                                bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_400),
                                border_radius=8
                            )
                        ], spacing=10),
                        padding=15
                    )
                )
            )
        
        page.update()
    
    graficos_tab = ft.Column([
        ft.Row([
            ft.Text("Análise de Preços", size=20, weight=ft.FontWeight.BOLD),
            ft.IconButton(
                icon=ft.icons.REFRESH,
                tooltip="Atualizar",
                on_click=lambda e: atualizar_graficos()
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        graficos_view
    ], expand=True)
    
    alertas_view = ft.ListView(expand=True, spacing=12, padding=15)
    
    def atualizar_alertas():
        alertas_view.controls.clear()
        
        if not data["favorites"]:
            alertas_view.controls.append(
                ft.Container(
                    content=ft.Text("Adicione favoritos para criar alertas", size=16),
                    alignment=ft.alignment.center,
                    expand=True
                )
            )
            page.update()
            return
        
        for fav in data["favorites"]:
            product_id = fav.get("id")
            alert = next((a for a in data["alerts"] if a["product_id"] == product_id), None)
            
            def criar_alerta(e, pid=product_id, titulo=fav["titulo"]):
                def salvar_alerta(ee):
                    try:
                        threshold = float(dlg_price.value.replace(",", "."))
                        data["alerts"].append({
                            "product_id": pid,
                            "threshold_price": threshold,
                            "enabled": True,
                            "created_at": datetime.now().strftime("%d/%m/%Y")
                        })
                        save_data(data)
                        dlg.open = False
                        atualizar_alertas()
                        page.update()
                    except:
                        pass
                
                dlg_price = ft.TextField(label="Preço desejado (R$)", keyboard_type=ft.KeyboardType.NUMBER)
                dlg = ft.AlertDialog(
                    title=ft.Text("Criar Alerta"),
                    content=ft.Column([
                        ft.Text(f"{titulo[:60]}", size=14),
                        dlg_price
                    ], tight=True, height=120),
                    actions=[
                        ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg, 'open', False) or page.update()),
                        ft.ElevatedButton("Criar", on_click=salvar_alerta)
                    ]
                )
                page.open(dlg)
            
            def toggle_alerta(e, pid=product_id):
                alert = next((a for a in data["alerts"] if a["product_id"] == pid), None)
                if alert:
                    alert["enabled"] = not alert["enabled"]
                    save_data(data)
                    atualizar_alertas()
            
            def remover_alerta(e, pid=product_id):
                data["alerts"] = [a for a in data["alerts"] if a["product_id"] != pid]
                save_data(data)
                atualizar_alertas()
            
            if alert:
                alertas_view.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row([
                                ft.Icon(
                                    ft.icons.NOTIFICATIONS_ACTIVE if alert["enabled"] else ft.icons.NOTIFICATIONS_OFF,
                                    color=ft.colors.ORANGE_400 if alert["enabled"] else ft.colors.GREY_400
                                ),
                                ft.Column([
                                    ft.Text(fav["titulo"][:60], size=14, weight=ft.FontWeight.BOLD),
                                    ft.Text(
                                        f"Alertar quando ≤ R$ {alert['threshold_price']:.2f}",
                                        size=12,
                                        color=ft.colors.GREY_400
                                    )
                                ], expand=True),
                                ft.Switch(value=alert["enabled"], on_change=toggle_alerta),
                                ft.IconButton(icon=ft.icons.DELETE, on_click=remover_alerta)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=12
                        )
                    )
                )
            else:
                alertas_view.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.icons.ADD_ALERT, color=ft.colors.GREY_400),
                                ft.Column([
                                    ft.Text(fav["titulo"][:60], size=14, weight=ft.FontWeight.BOLD),
                                    ft.Text("Sem alerta", size=12, color=ft.colors.GREY_400)
                                ], expand=True),
                                ft.ElevatedButton("Criar", on_click=criar_alerta)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=12
                        )
                    )
                )
        
        page.update()
    
    alertas_tab = ft.Column([
        ft.Row([
            ft.Text("Alertas de Preço", size=20, weight=ft.FontWeight.BOLD),
            ft.IconButton(
                icon=ft.icons.REFRESH,
                tooltip="Atualizar",
                on_click=lambda e: atualizar_alertas()
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Container(
            content=ft.Text(
                "Configure alertas para ser notificado quando o preço baixar",
                size=13,
                color=ft.colors.BLUE_400
            ),
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_400),
            padding=10,
            border_radius=8
        ),
        alertas_view
    ], expand=True)
    
    txt_api_key = ft.TextField(
        label="SerpAPI Key (opcional)",
        value=config.get("serpapi_key", ""),
        password=True,
        can_reveal_password=True,
        expand=True,
        hint_text="Cole sua chave da SerpAPI aqui"
    )
    
    def salvar_config(e):
        config["serpapi_key"] = txt_api_key.value.strip()
        save_config(config)
        page.show_snack_bar(ft.SnackBar(ft.Text("✅ Configurações salvas!")))
    
    def testar_api(e):
        async def teste():
            key = txt_api_key.value.strip()
            if not key:
                page.show_snack_bar(ft.SnackBar(ft.Text("Digite a chave primeiro")))
                return
            
            try:
                url = "https://serpapi.com/search.json"
                params = {"engine": "google_shopping", "q": "teste", "api_key": key}
                async with httpx.AsyncClient(timeout=10) as client:
                    r = await client.get(url, params=params)
                    if r.status_code == 200:
                        page.show_snack_bar(ft.SnackBar(
                            ft.Text("✅ Chave válida!"),
                            bgcolor=ft.colors.GREEN_700
                        ))
                    else:
                        page.show_snack_bar(ft.SnackBar(
                            ft.Text("❌ Chave inválida"),
                            bgcolor=ft.colors.RED_700
                        ))
            except:
                page.show_snack_bar(ft.SnackBar(
                    ft.Text("❌ Erro ao testar"),
                    bgcolor=ft.colors.RED_700
                ))
        
        asyncio.create_task(teste())
    
    config_tab = ft.Column([
        ft.Text("Configurações", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text("API do Google Shopping", size=18, weight=ft.FontWeight.BOLD),
        ft.Text(
            "Para buscar no Google Shopping, você precisa de uma chave da SerpAPI.\n"
            "1. Crie conta grátis em: serpapi.com\n"
            "2. Pegue sua API key no dashboard\n"
            "3. Cole abaixo (100 buscas/mês grátis)",
            size=14,
            color=ft.colors.GREY_400
        ),
        ft.Row([
            txt_api_key,
            ft.ElevatedButton("Testar", on_click=testar_api),
            ft.ElevatedButton("Salvar", on_click=salvar_config, style=ft.ButtonStyle(
                bgcolor=ft.colors.GREEN_700
            ))
        ], spacing=10),
        ft.Divider(),
        ft.Text("Cache", size=18, weight=ft.FontWeight.BOLD),
        ft.Text(f"Validade do cache: {CACHE_TTL // 60} minutos", size=14),
        ft.ElevatedButton(
            "Limpar cache",
            icon=ft.icons.CLEANING_SERVICES,
            on_click=lambda e: (
                cache.clear(),
                save_cache(cache),
                page.show_snack_bar(ft.SnackBar(ft.Text("✅ Cache limpo!")))
            )
        ),
        ft.Divider(),
        ft.Text("Sobre", size=18, weight=ft.FontWeight.BOLD),
        ft.Text("Caçador de Preços v5.0", size=14, weight=ft.FontWeight.BOLD),
        ft.Text("Compare preços e economize!", size=14, color=ft.colors.GREY_400),
        ft.TextButton("GitHub", on_click=lambda e: page.launch_url("https://github.com/seu-usuario/cacador-precos"))
    ], expand=True, spacing=15, scroll=ft.ScrollMode.AUTO)
    
    content_container = ft.Container(expand=True)
    
    def update_tab_content():
        if tabs.selected_index == 0:
            content_container.content = busca_tab
        elif tabs.selected_index == 1:
            content_container.content = historico_tab
            atualizar_historico()
        elif tabs.selected_index == 2:
            content_container.content = favoritos_tab
            atualizar_favoritos()
        elif tabs.selected_index == 3:
            content_container.content = graficos_tab
            atualizar_graficos()
        elif tabs.selected_index == 4:
            content_container.content = alertas_tab
            atualizar_alertas()
        elif tabs.selected_index == 5:
            content_container.content = config_tab
        page.update()
    
    tabs.on_change = lambda e: update_tab_content()
    update_tab_content()
    
    def exportar_csv(e):
        if not current_results:
            page.show_snack_bar(ft.SnackBar(ft.Text("Faça uma busca primeiro")))
            return
        try:
            filename = f"precos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Loja", "Produto", "Preço (R$)", "Frete Grátis", "Link"])
                for r in current_results:
                    writer.writerow([
                        r["loja"],
                        r["titulo"],
                        r["preco"],
                        "Sim" if r.get("frete_gratis") else "Não",
                        r["link"]
                    ])
            page.show_snack_bar(ft.SnackBar(ft.Text(f"✅ Exportado: {filename}")))
        except Exception as ex:
            page.show_snack_bar(ft.SnackBar(ft.Text(f"Erro: {ex}")))
    
    page.appbar = ft.AppBar(
        title=ft.Text("Caçador de Preços"),
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(
                icon=ft.icons.FILE_DOWNLOAD,
                tooltip="Exportar CSV",
                on_click=exportar_csv
            ),
            ft.IconButton(
                icon=ft.icons.BRIGHTNESS_6,
                tooltip="Tema",
                on_click=lambda e: (
                    setattr(page, "theme_mode", ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK),
                    page.update()
                )
            )
        ]
    )
    
    page.add(
        ft.Column([
            tabs,
            content_container
        ], expand=True, spacing=0)
    )
    
    txt_busca.on_submit = buscar

def run_app():
    ft.run(target=main)

if __name__ == "__main__":
    ft.run(target=main)
