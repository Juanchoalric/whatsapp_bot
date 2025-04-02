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
        """Buscar productos por nombre (búsqueda parcial)"""
        return self.db.query(Product).filter(Product.name.ilike(f"%{name}%")).all()
    
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
            
        result = "📋 CATÁLOGO DE PRODUCTOS:\n\n"
        for product in products:
            stock_status = "✅ En stock" if product.stock > 0 else "❌ Agotado"
            result += f"• {product.name}\n  💲 ${product.price:.2f}\n  📦 {stock_status}\n\n"
            
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
            return f"{product.name}: ${product.price:.2f}. {product.description} - {product.stock} unidades en stock."
        else:
            result = f"Encontré {len(products)} productos que coinciden con '{name}':\n\n"
            for product in products:
                result += f"- {product.name}: ${product.price:.2f} - {product.stock} unidades en stock\n"
            return result 