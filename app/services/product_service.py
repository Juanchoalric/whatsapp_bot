from sqlalchemy.orm import Session
from app.models.product import Product
from typing import List, Optional

class ProductService:
    """
    Servicio para gestionar los productos en la base de datos
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_products(self) -> List[Product]:
        """Obtener todos los productos"""
        return self.db.query(Product).all()
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Obtener un producto por su ID"""
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def get_products_by_name(self, name: str) -> List[Product]:
        """Buscar productos por nombre (búsqueda parcial) con tolerancia a errores comunes"""
        # Corregir errores comunes de escritura
        search_name = name.lower()
        corrections = {
            "chuchillo": "cuchillo",
            "cuchilo": "cuchillo",
            "cuchiyos": "cuchillos",
            "cuvhillo": "cuchillo",
            "cucillo": "cuchillo",
            "santoco": "santoku",
            "zantoku": "santoku",
            "santuko": "santoku"
        }
        
        # Aplicar correcciones
        for error, correction in corrections.items():
            if error in search_name:
                search_name = search_name.replace(error, correction)
        
        # Primero intentar una búsqueda exacta normalizada
        products = self.db.query(Product).filter(Product.name.ilike(f"%{search_name}%")).all()
        
        # Si no encontramos nada, intentar búsquedas parciales con palabras clave
        if not products and " " in search_name:
            # Dividir en palabras clave y buscar cada una
            keywords = [word for word in search_name.split() if len(word) > 3]
            if keywords:
                for keyword in keywords:
                    products_by_keyword = self.db.query(Product).filter(Product.name.ilike(f"%{keyword}%")).all()
                    if products_by_keyword:
                        return products_by_keyword
        
        return products
    
    def get_product_details_as_text(self, product_id: int) -> str:
        """
        Obtener los detalles de un producto como texto formateado
        para ser usado en respuestas
        """
        product = self.get_product_by_id(product_id)
        if not product:
            return "Producto no encontrado."
        
        return f"""
        Nombre: {product.name}
        Precio: ${product.price:.2f}
        Descripción: {product.description}
        Disponibilidad: {'En stock' if product.stock > 0 else 'Agotado'}
        """
    
    def get_products_by_search(self, search_term: str) -> List[Product]:
        """
        Buscar productos por término de búsqueda en nombre y descripción
        """
        return self.db.query(Product).filter(
            (Product.name.ilike(f"%{search_term}%")) | 
            (Product.description.ilike(f"%{search_term}%"))
        ).all()
    
    def get_products_in_price_range(self, min_price: float, max_price: float) -> List[Product]:
        """
        Obtener productos en un rango de precios
        """
        return self.db.query(Product).filter(
            Product.price >= min_price,
            Product.price <= max_price
        ).all()
        
    def get_all_products_text(self) -> str:
        """
        Obtener todos los productos como texto formateado
        """
        products = self.get_all_products()
        if not products:
            return "No hay productos disponibles."
            
        result = "CATÁLOGO DE PRODUCTOS:\n\n"
        for product in products:
            stock_status = "En stock" if product.stock > 0 else "Agotado"
            result += f"• {product.name}\n  Precio: ${product.price:.2f}\n  Estado: {stock_status}\n\n"
            
        return result
        
    def get_product_info_by_name(self, name: str) -> str:
        """
        Obtener información de un producto por su nombre
        """
        products = self.get_products_by_name(name)
        if not products:
            return f"No se encontró ningún producto que coincida con '{name}'."
            
        if len(products) == 1:
            product = products[0]
            stock_status = f"{product.stock} unidades en stock" if product.stock > 0 else "Agotado"
            return f"""{product.name}
Precio: ${product.price:.2f}
{product.description}
Stock: {stock_status}"""
        else:
            result = f"Encontré {len(products)} productos que coinciden con '{name}':\n\n"
            for product in products:
                stock_status = f"{product.stock} unidades en stock" if product.stock > 0 else "Agotado"
                result += f"""{product.name}
Precio: ${product.price:.2f}
Stock: {stock_status}

"""
            return result 