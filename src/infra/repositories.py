import requests
from sqlalchemy.orm import Session

from src.domain.models import ProductCreate, Product


class ProductRepository:

    def __init__(self, db: Session):
        self.db = db

    # Dentro da classe ProductRepository:
    def create(self, product: ProductCreate):
        # 1. Converte o objeto Pydantic em um dicionário para enviar na requisição
        # Ignoramos o ID (a API externa quem gera) e o rating (ela não aceita no POST)
        payload = {
            "title": product.title,
            "price": product.price,
            "description": product.description,
            "category": product.category,
            "image": product.image
        }

        try:
            # 2. Dispara o POST para a Fake Store API
            resposta = requests.post("https://fakestoreapi.com/products", json=payload, timeout=10)

            # 3. Verifica se a API externa aceitou a criação
            if resposta.status_code in [200, 201]:
                # A API retorna o objeto criado contendo o novo 'id' gerado por eles
                dados_api = resposta.json()

                # 4. Cria a entidade para o banco local usando o ID que a Fake Store retornou
                novo_produto = Product(
                    id=dados_api.get("id"),
                    title=product.title,
                    price=product.price,
                    description=product.description,
                    category=product.category,
                    image=product.image,
                    stock=product.stock if product.stock else 0,
                    # Como a FakeStore não recebe rating na criação, definimos valores iniciais
                    rating_rate=product.rating.rate if product.rating else 0.0,
                    rating_count=product.rating.count if product.rating else 0
                )

                # 5. Salva no banco SQLite
                self.db.add(novo_produto)
                self.db.commit()
                self.db.refresh(novo_produto)

                return novo_produto
            else:
                raise ValueError(f"Falha na API Externa. Status: {resposta.status_code}")

        except requests.exceptions.RequestException as e:
            # Evita que a aplicação quebre caso esteja sem internet ou a API caia
            print(f"Erro de comunicação com a Fake Store API: {e}")
            raise Exception("Não foi possível conectar ao serviço de catálogo global.")

    def list(self):
        return self.db.query(Product).all()

    def listAndAtualizarExterno(self):
        produtos_externos = self.buscar_dados_api_externa()
        if produtos_externos:
            for item in produtos_externos:
                    # Busca pelo ID em vez do título
                produto_db = self.db.query(Product).filter(Product.id == item['id']).first()

                if produto_db:
                    print(f"Produto {item['title']} já existe no banco de dados.")
                    continue
                else:
                    # Se não existe, insere o novo produto (Insert)
                    novo_produto = Product(
                        id=item['id'],
                        title=item['title'],
                        price=float(item['price']),
                        description=item['description'],
                        category=item['category'],
                        image=item['image'],
                        rating_rate=float(item['rating']['rate']),
                        rating_count=int(item['rating']['count']),
                        stock=0,
                    )
                    self.db.add(novo_produto)
                    self.db.commit()
        return self.db.query(Product).all()

    def find_by_id(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()

    def update(self, product_id: int, product_in):
        # 1. Transforma os dados recebidos em dicionário, ignorando valores não enviados
        update_data = product_in.model_dump(exclude_unset=True)

        # 2. Se houver o campo 'rating' na requisição de atualização, nós o desmembramos
        if 'rating' in update_data:
            rating_data = update_data.pop('rating') # Remove 'rating' do dicionário principal
            if rating_data:
                update_data['rating_rate'] = rating_data['rate']
                update_data['rating_count'] = rating_data['count']
    
        # 3. Executa o update no SQLAlchemy apenas com colunas reais do banco
        if update_data:
            self.db.query(Product).filter(Product.id == product_id).update(update_data)
            self.db.commit()

        # 4. Retorna o produto atualizado
        return self.db.query(Product).filter(Product.id == product_id).first()

    def delete(self, product_id: int):
        self.db.query(Product).filter(Product.id == product_id).delete()
        self.db.commit()

    def buscar_dados_api_externa(self):
        resp = requests.get("https://fakestoreapi.com/products", timeout=5)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception("Erro ao buscar dados da API externa")