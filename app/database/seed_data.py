from sqlalchemy.orm import Session
from app.models.product import Product
from app.database.database import engine, Base, SessionLocal

def seed_database():
    """
    Crea las tablas y añade datos iniciales a la base de datos
    """
    # Crear tablas primero, antes de cualquier consulta
    Base.metadata.create_all(bind=engine)
    
    # Añadir productos de ejemplo
    db = SessionLocal()
    
    try:
        # Comprobar si ya hay productos
        if db.query(Product).count() == 0:
            products = [
                Product(
                    name="Cuchillo Chef Premium",
                    description="Cuchillo de chef profesional forjado con acero alemán de alta calidad. Hoja de 20cm perfecta para todo tipo de cortes. Mango ergonómico que proporciona comodidad y control.",
                    price=89.99,
                    stock=25,
                    image_url="https://example.com/images/chef_premium.jpg"
                ),
                Product(
                    name="Set de Cuchillos Básico",
                    description="Conjunto de 5 cuchillos esenciales para cualquier cocina. Incluye cuchillo de chef, cuchillo para pan, cuchillo de utilidad, cuchillo para pelar y tijeras de cocina.",
                    price=129.99,
                    stock=15,
                    image_url="https://example.com/images/basic_set.jpg"
                ),
                Product(
                    name="Cuchillo Santoku",
                    description="Cuchillo japonés versátil con hoja de 18cm. Ideal para cortar, picar y rebanar con alta precisión. Acero inoxidable con filo duradero.",
                    price=65.50,
                    stock=30,
                    image_url="https://example.com/images/santoku.jpg"
                ),
                Product(
                    name="Cuchillo para Pan",
                    description="Cuchillo con hoja serrada de 22cm, diseñado específicamente para cortar pan de forma limpia sin aplastar. Mango de madera natural.",
                    price=45.00,
                    stock=20,
                    image_url="https://example.com/images/bread_knife.jpg"
                ),
                Product(
                    name="Cuchillo de Carne Premium",
                    description="Cuchillo para carne con hoja de 15cm, perfecto para trinchar y cortar carnes con facilidad. Acero de alta calidad con excelente retención del filo.",
                    price=78.50,
                    stock=18,
                    image_url="https://example.com/images/meat_knife.jpg"
                ),
                Product(
                    name="Cuchillo Puntilla",
                    description="Cuchillo pequeño con hoja de 9cm, ideal para trabajos de precisión como pelar, decorar y trabajos detallados. Mango ergonómico antideslizante.",
                    price=32.99,
                    stock=40,
                    image_url="https://example.com/images/paring_knife.jpg"
                ),
                Product(
                    name="Set de Cuchillos Profesional",
                    description="Conjunto completo de 12 piezas para el chef profesional. Incluye bloque de madera, afilador y variedad de cuchillos especializados.",
                    price=299.99,
                    stock=8,
                    image_url="https://example.com/images/pro_set.jpg"
                )
            ]
            
            db.add_all(products)
            db.commit()
            print("Base de datos poblada con productos de ejemplo")
    except Exception as e:
        print(f"Error al poblar la base de datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database() 