from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    products = relationship('Product', back_populates='category', cascade="all, delete-orphan")

    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}')"


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='products')

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, category_id={self.category_id})"


engine = create_engine('sqlite:///test.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def create_category(name):
    category = Category(name=name)
    session.add(category)
    session.commit()
    return category


def create_product(name, price, category_id):
    product = Product(name=name, price=price, category_id=category_id)
    session.add(product)
    session.commit()
    return product


def get_products_by_category(category_id):
    products = session.query(Product).filter_by(category_id=category_id).all()
    return products


def update_product_category(product_id, new_category_id):
    product = session.query(Product).get(product_id)
    if product:
        product.category_id = new_category_id
        session.commit()
        return product
    return None


def delete_category_and_products(category_id):
    category = session.query(Category).get(category_id)
    if category:
        session.delete(category)
        session.commit()


# Example usage
if __name__ == "__main__":
    # создание категорий
    cat1 = create_category("Electronics")
    cat2 = create_category("Clothing")

    # создание продуктов
    prod1 = create_product("Laptop", 999.99, cat1.id)
    prod2 = create_product("Smartphone", 499.99, cat1.id)
    prod3 = create_product("Jeans", 39.99, cat2.id)

    # получить продукт по категории
    electronics_products = get_products_by_category(cat1.id)
    print("Electronics Products:", electronics_products)

    # обновить категорию
    updated_product = update_product_category(prod3.id, cat1.id)
    print("Updated Product:", updated_product)

    # удалить категорию и продукты
    delete_category_and_products(cat2.id)
    print("Categories after deletion:", session.query(Category).all())
    print("Products after deletion:", session.query(Product).all())
