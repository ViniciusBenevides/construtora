# app.py

# 1. Importa bibliotecas: Flask e a extensão de Banco de Dados
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    LoginManager,
    login_user,
    logout_user,
    current_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename  # Para nomes de arquivo seguros
import os  # Para manipular caminhos de arquivo

# --- CONFIGURAÇÃO DO FLASK ---
app = Flask(__name__)

app.config["SECRET_KEY"] = "uma-chave-muito-secreta-e-unica"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///imobiliaria.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Diretório para salvar as imagens (aponta para a pasta 'static/fotos_imoveis')
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static/fotos_imoveis")
# Extensões permitidas
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}


# Funções auxiliares para upload
def allowed_file(filename):
    # Checa se o arquivo tem um ponto (.) e se a parte após o ponto (extensão) está nas permitidas
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


# 3. Cria os objetos de Extensão
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # Inicializa a criptografia
login_manager = LoginManager()  # Inicializa o gerenciador de login SEM o APP!
login_manager.init_app(app)  # Configura o gerenciador de login com o app
login_manager.login_view = "login"


# Função necessária para o Flask-Login carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    # Retorna o objeto Usuario que corresponde ao ID salvo na sessão
    return Usuario.query.get(int(user_id))


# --- MODELO (A ESTRUTURA) DO IMÓVEL ---
# 4. Cria uma "Classe" (um molde) para o Imóvel
#    Esta classe representa uma "tabela" no nosso Banco de Dados
class Imovel(db.Model):
    # Campos que definem cada imóvel (as colunas da tabela)

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    tipo_imovel = db.Column(db.String(50), nullable=False)
    quartos = db.Column(db.Integer, default=1)
    vagas = db.Column(db.Integer, default=0)
    banheiros = db.Column(db.Integer, default=1)
    area_m2 = db.Column(db.Float, default=0.0)
    valor = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pronto")
    # NOVO CAMPO: Chave Estrangeira que aponta para o ID do usuário
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    # NOVO CAMPO: Caminho da foto principal (será uma string)
    foto_principal = db.Column(db.String(100), default="default.png")

    # RELACIONAMENTO: Permite acessar o objeto Usuario a partir do Imovel
    autor = db.relationship("Usuario", backref="imoveis", lazy=True)

    # NOVO: Método construtor (inicializador) para clareza e para o Pylance
    def __init__(
        self,
        codigo,
        cidade,
        bairro,
        tipo_imovel,
        quartos,
        vagas,
        banheiros,
        area_m2,
        valor,
        status,
        usuario_id,
        foto_principal="default.png",
    ):
        self.codigo = codigo
        self.cidade = cidade
        self.bairro = bairro
        self.tipo_imovel = tipo_imovel
        self.quartos = quartos
        self.vagas = vagas
        self.banheiros = banheiros
        self.area_m2 = area_m2
        self.valor = valor
        self.status = status
        self.usuario_id = usuario_id
        self.foto_principal = foto_principal

    def __repr__(self):
        return f"Imovel('{self.tipo_imovel}', Cód: {self.codigo}, {self.cidade})"


# --- NOVO MODELO (A ESTRUTURA) DO USUÁRIO ---
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    funcao = db.Column(db.String(20), default="Corretor")

    # NOVO: Método construtor (inicializador) para clareza e para o Pylance
    def __init__(self, username, email, senha_hash, funcao):
        self.username = username
        self.email = email
        self.senha_hash = senha_hash
        self.funcao = funcao

    # Método para verificar a senha
    def verificar_senha(self, senha_texto_claro):
        return bcrypt.check_password_hash(self.senha_hash, senha_texto_claro)

    def __repr__(self):
        return f"Usuario('{self.username}', '{self.funcao}')"


# --- ROTAS DO SITE (O que acontece quando o usuário acessa) ---


@app.route("/")
def pagina_inicial():
    # 1. BUSCA: Pede ao Banco de Dados para encontrar todos os objetos Imovel
    imoveis = Imovel.query.all()
    # 2. ENVIA: Passa a lista de 'imoveis' para o arquivo 'index.html'
    #    No HTML, você poderá usar a variável chamada 'imoveis'
    return render_template("index.html", imoveis=imoveis)


# NOVA ROTA DE CADASTRO
# methods=['GET', 'POST'] permite que a mesma função lide com
# a exibição (GET) e o envio de dados (POST) do formulário.
@app.route("/cadastrar", methods=["GET", "POST"])
@login_required  # <--- ESSA LINHA PROTEGE A ROTA
def cadastrar_imovel():
    # Se o usuário tentar acessar esta rota sem login,
    # ele será redirecionado para a rota 'login' (o que definimos em login_view)

    # 1. (NOVO) Verificação de permissão: Apenas Admin ou Corretor podem cadastrar
    if current_user.funcao not in ["Admin", "Corretor"]:
        flash(
            "Você não tem permissão para acessar a área de cadastro de imóveis.",
            "error",
        )
        return redirect(url_for("pagina_inicial"))
    # Se o método for POST, significa que o usuário enviou o formulário
    if request.method == "POST":
        dados = request.form

        # 1. TRATAMENTO DO ARQUIVO DE UPLOAD
        caminho_foto = "default.jpg"
        # Verifica se o campo 'foto' foi enviado (tem que estar no HTML!)
        if "foto" in request.files:
            foto = request.files["foto"]

            # Verifica se há um arquivo e se a extensão é permitida
            if foto and allowed_file(foto.filename):
                # Cria um nome seguro para o arquivo
                filename = secure_filename(foto.filename)
                # Monta o caminho completo onde o arquivo será salvo
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                # Salva o arquivo no disco!
                foto.save(filepath)
                caminho_foto = filename  # Guardamos apenas o nome para o BD

        # 2. Cria o novo objeto Imovel (agora incluindo foto_principal)
        novo_imovel = Imovel(
            codigo=dados["codigo"],
            cidade=dados["cidade"],
            bairro=dados["bairro"],
            tipo_imovel=dados["tipo_imovel"],
            quartos=int(dados["quartos"]),
            vagas=int(dados["vagas"]),
            banheiros=int(dados["banheiros"]),
            area_m2=float(dados["area_m2"]),
            valor=float(dados["valor"]),
            status=dados["status"],
            usuario_id=current_user.id,
            foto_principal=caminho_foto,  # <--- NOVO
        )

        # 2. BLOCO TRY/EXCEPT PARA LIDAR COM ERROS DE BANCO DE DADOS
        try:
            # Tenta adicionar e salvar no Banco de Dados
            db.session.add(novo_imovel)
            db.session.commit()

            # Se for bem-sucedido:
            flash(f"Imóvel {novo_imovel.codigo} cadastrado com sucesso!", "success")

        except Exception as e:
            # Se der erro (ex: código duplicado), desfaz a operação no BD
            db.session.rollback()

            # Mensagem mais amigável para o usuário
            if "UNIQUE constraint failed" in str(e):
                flash(
                    f"ERRO: O código de imóvel '{dados['codigo']}' já está em uso. Por favor, use um código diferente.",
                    "error",
                )
            else:
                flash(
                    "Ocorreu um erro ao tentar salvar o imóvel. Tente novamente.",
                    "error",
                )

        # 3. Redireciona sempre, para evitar reenvio do formulário
        return redirect(url_for("cadastrar_imovel"))

    # Se o método for GET, apenas exibe a página do formulário
    return render_template("cadastro_imovel.html")


# O <status_filtro> permite que a URL aceite diferentes valores
@app.route("/imoveis/<status_filtro>")
def listar_imoveis_por_status(status_filtro):
    # 1. Lógica para determinar o filtro de busca no BD

    # Mapeamento do que está na URL para o valor que está no BD
    mapeamento_status = {
        "alugar": "Para Alugar",
        "lancamentos": "Lançamento",
        "prontos": "Pronto",
        "portfolio": "Todos",  # 'Todos' é um status especial, não é um filtro real
    }

    status_db = mapeamento_status.get(status_filtro)

    # 2. Busca no Banco de Dados
    if status_db and status_db != "Todos":
        # VOLTANDO AO PADRÃO ANTIGO/COMPATÍVEL DO FLASK-SQLALCHEMY
        # para silenciar o Pylance nos filtros simples
        imoveis = Imovel.query.filter_by(status=status_db).all()
        titulo_pagina = f"Imóveis - {status_db}"
    elif status_filtro == "portfolio":
        imoveis = Imovel.query.all()
        titulo_pagina = "Portfólio Completo de Imóveis"
    else:
        imoveis = []
        titulo_pagina = "Categoria Não Encontrada"

    # 3. Renderiza a mesma página inicial, mas com os imóveis filtrados
    return render_template("index.html", imoveis=imoveis, titulo=titulo_pagina)


# --- ROTA DE BUSCA E FILTRO AVANÇADO ---
@app.route("/buscar", methods=["GET"])
def buscar_imoveis():
    filtros = request.args
    query = db.select(
        Imovel
    )  # NOVO: Iniciando a consulta com db.select(Imovel) para clareza

    # 2. Aplica os filtros dinamicamente

    # Filtro por Cidade
    cidade = filtros.get("cidade")
    if cidade:
        # AGORA USAMOS .filter_by() OU .filter() COM A SINTAXE DE CLASSE
        # db.select().where() é a forma mais moderna e que agrada o Pylance/SQLAlchemy 2.0
        query = query.filter(Imovel.cidade.ilike(f"%{cidade}%"))

    # Filtro por Bairro
    bairro = filtros.get("bairro")
    if bairro:
        query = query.filter(Imovel.bairro.ilike(f"%{bairro}%"))

    # Filtro por Tipo de Imóvel
    tipo = filtros.get("tipo")
    if tipo:
        query = query.filter(Imovel.tipo_imovel == tipo)  # Usando == para igualdade

    # Filtro por Valor Mínimo
    min_valor = filtros.get("min_valor")
    if min_valor:
        try:
            query = query.filter(Imovel.valor >= float(min_valor))
        except ValueError:
            pass

    # Filtro por Valor Máximo
    max_valor = filtros.get("max_valor")
    if max_valor:
        try:
            query = query.filter(Imovel.valor <= float(max_valor))
        except ValueError:
            pass

    # Filtro por Quartos Mínimos
    quartos_min = filtros.get("quartos")
    if quartos_min:
        try:
            query = query.filter(Imovel.quartos >= int(quartos_min))
        except ValueError:
            pass

    # Filtro por Vagas Mínimas
    vagas_min = filtros.get("vagas")
    if vagas_min:
        try:
            query = query.filter(Imovel.vagas >= int(vagas_min))
        except ValueError:
            pass

    # 3. Executa a busca no Banco de Dados
    # db.session.execute(query) executa a query e retorna resultados
    # .scalars().all() extrai apenas os objetos Imovel da resposta
    imoveis_encontrados = db.session.execute(query).scalars().all()

    # 4. Retorna a página de busca com os resultados
    return render_template("busca.html", imoveis=imoveis_encontrados)


# --- NOVA ROTA DE DETALHES DO IMÓVEL (ETAPA 7) ---
@app.route("/imovel/<codigo>")
def detalhes_imovel(codigo):
    # 1. Busca no Banco de Dados pelo código do imóvel (que é único)
    # .first_or_404() significa: encontre o primeiro resultado OU retorne um erro 404 (Não Encontrado)
    imovel = Imovel.query.filter_by(codigo=codigo).first_or_404()

    # 2. Renderiza a página de detalhes, enviando o objeto 'imovel'
    return render_template("detalhes.html", imovel=imovel)


# --- ROTA DE EDIÇÃO DE IMÓVEL ---
@app.route("/imovel/editar/<codigo>", methods=["GET", "POST"])
@login_required  # Protegemos esta rota também!
def editar_imovel(codigo):
    # 1. Busca o imóvel a ser editado
    imovel = Imovel.query.filter_by(codigo=codigo).first_or_404()

    # 2. (NOVO) Verificação de permissão: Apenas Admin pode editar QUALQUER imóvel
    #    (No futuro, um Corretor só poderia editar os seus próprios)
    if current_user.funcao != "Admin":
        flash(
            "Você não tem permissão de administrador para editar este imóvel.", "error"
        )
        return redirect(url_for("detalhes_imovel", codigo=codigo))

    if request.method == "POST":
        # Recebe os dados do formulário
        dados = request.form

        try:
            # 3. Atualiza os atributos do objeto imóvel
            imovel.cidade = dados["cidade"]
            imovel.bairro = dados["bairro"]
            imovel.tipo_imovel = dados["tipo_imovel"]
            imovel.quartos = int(dados["quartos"])
            imovel.vagas = int(dados["vagas"])
            imovel.banheiros = int(dados["banheiros"])
            imovel.area_m2 = float(dados["area_m2"])
            imovel.valor = float(dados["valor"])
            imovel.status = dados["status"]
            # NOTA: O código (ID) não é alterado, apenas as informações.

            # Salva as alterações
            db.session.commit()
            flash(f"Imóvel {imovel.codigo} atualizado com sucesso!", "success")
            return redirect(url_for("detalhes_imovel", codigo=imovel.codigo))

        except Exception as e:
            db.session.rollback()
            flash("Ocorreu um erro ao atualizar o imóvel. Tente novamente.", "error")
            # Você pode logar (imprimir) o erro 'e' para debugar se necessário

    # Se for GET, renderiza a página de edição (usaremos o mesmo template de cadastro)
    # Passamos o objeto 'imovel' para o template preencher os campos.
    return render_template(
        "cadastro_imovel.html", imovel=imovel, titulo="Editar Imóvel"
    )


# --- ROTA DE EXCLUSÃO DE IMÓVEL ---
@app.route("/imovel/excluir/<codigo>", methods=["POST"])
@login_required  # Protegemos esta rota!
def excluir_imovel(codigo):
    # 1. Busca o imóvel
    imovel = Imovel.query.filter_by(codigo=codigo).first_or_404()

    # 2. Verificação de permissão (apenas Admin)
    if current_user.funcao != "Admin":
        flash("Você não tem permissão para excluir imóveis.", "error")
        return redirect(url_for("detalhes_imovel", codigo=codigo))

    # 3. Deleta o imóvel
    db.session.delete(imovel)
    db.session.commit()
    flash(f"Imóvel {codigo} excluído permanentemente.", "success")

    # Redireciona para a página inicial (ou para a lista de imóveis)
    return redirect(url_for("pagina_inicial"))


# --- ROTA DE LOGIN (PARA O MODAL FUNCIONAR) ---
@app.route("/login", methods=["GET", "POST"])
def login():
    # Redireciona se o usuário já estiver logado
    if current_user.is_authenticated:
        return redirect(url_for("pagina_inicial"))

    # Se o formulário foi submetido (POST)
    if request.method == "POST":
        # Pega dados do formulário
        email_ou_user = request.form["email_ou_user"]
        senha = request.form["senha"]

        # 1. Tenta encontrar o usuário pelo email OU username
        usuario = Usuario.query.filter(
            (Usuario.email == email_ou_user) | (Usuario.username == email_ou_user)
        ).first()

        # 2. Verifica se o usuário existe E se a senha está correta
        if usuario and usuario.verificar_senha(senha):
            # Login bem-sucedido
            login_user(usuario)
            flash("Login bem-sucedido!", "success")

            # Redireciona para onde o usuário tentou ir antes de ser pego pelo login
            next_page = request.args.get("next")
            return redirect(next_page or url_for("pagina_inicial"))
        else:
            # Login falhou
            flash("Login falhou. Verifique seu e-mail/usuário e senha.", "error")

    # Se for GET ou o login falhou, mostra a página de login
    # Por enquanto, vamos usar um template de login dedicado, já que o modal é só visual.
    # Se houver uma falha de login (depois do POST) ou se for um acesso direto por GET,
    # ele redireciona para a página inicial, onde o modal deve ser ativado pelo JS/Flash.
    return redirect(url_for("pagina_inicial"))


# --- ROTA DE LOGOUT ---
@app.route("/logout")
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for("pagina_inicial"))


# --- ROTA DO DASHBOARD (ETAPA 11) ---
@app.route("/dashboard")
@login_required  # Só acessa se estiver logado
def dashboard():
    # 1. Busca todos os imóveis CADASTRADOS POR ESTE USUÁRIO
    #    current_user.imoveis usa o relacionamento 'backref' que criamos na classe Imovel
    meus_imoveis = current_user.imoveis

    # Informações de resumo
    total_imoveis = len(meus_imoveis)
    imoveis_prontos = sum(1 for imovel in meus_imoveis if imovel.status == "Pronto")
    imoveis_alugar = sum(1 for imovel in meus_imoveis if imovel.status == "Para Alugar")

    return render_template(
        "dashboard.html",
        meus_imoveis=meus_imoveis,
        total_imoveis=total_imoveis,
        prontos=imoveis_prontos,
        alugar=imoveis_alugar,
        titulo="Meu Dashboard",
    )


# --- ROTA DE GERENCIAMENTO DE USUÁRIOS (ADMIN) ---
@app.route("/admin/usuarios", methods=["GET", "POST"])
@login_required
def gerenciar_usuarios():
    # 1. VERIFICAÇÃO DE PERMISSÃO: APENAS ADMIN PODE ACESSAR
    if current_user.funcao != "Admin":
        flash(
            "Acesso negado. Você precisa ser Administrador para gerenciar usuários.",
            "error",
        )
        return redirect(url_for("pagina_inicial"))

    # Se for POST, tentamos cadastrar um novo usuário
    if request.method == "POST":
        try:
            username = request.form["username"]
            email = request.form["email"]
            senha_texto = request.form["senha"]
            funcao = request.form["funcao"]

            # Verifica se o usuário/email já existe (simplesmente para dar feedback)
            if Usuario.query.filter(
                (Usuario.email == email) | (Usuario.username == username)
            ).first():
                flash(
                    "Erro: Já existe um usuário ou e-mail cadastrado com essas informações.",
                    "error",
                )
                # Se houver erro, recarrega a página com a lista atual
                usuarios = Usuario.query.all()
                return render_template(
                    "gerenciar_usuarios.html",
                    usuarios=usuarios,
                    titulo="Gerenciar Usuários",
                )

            # Criptografa a senha
            senha_criptografada = bcrypt.generate_password_hash(senha_texto).decode(
                "utf-8"
            )

            # Cria e salva o novo usuário
            novo_usuario = Usuario(
                username=username,
                email=email,
                senha_hash=senha_criptografada,
                funcao=funcao,
            )
            db.session.add(novo_usuario)
            db.session.commit()

            flash(f"Usuário {username} ({funcao}) criado com sucesso!", "success")
            return redirect(url_for("gerenciar_usuarios"))

        except Exception as e:
            db.session.rollback()
            flash("Ocorreu um erro inesperado ao cadastrar o usuário.", "error")

    # Se for GET, busca e exibe a lista de usuários e o formulário
    usuarios = Usuario.query.all()
    return render_template(
        "gerenciar_usuarios.html", usuarios=usuarios, titulo="Gerenciar Usuários"
    )


# --- INICIALIZAÇÃO DO SERVIDOR, DADOS DE TESTE E USUÁRIOS ---
if __name__ == "__main__":
    with app.app_context():
        # 1. Cria todas as tabelas (Imovel e Usuario)
        db.create_all()

        # VARIÁVEL TEMPORÁRIA para guardar o objeto admin_user
        admin_user = None

        # 2. Verifica e insere USUÁRIO ADMINISTRADOR DE TESTE (se vazio)
        if Usuario.query.count() == 0:
            print("Nenhum usuário encontrado. Criando usuário admin de teste...")

            senha_criptografada = bcrypt.generate_password_hash("123456").decode(
                "utf-8"
            )

            admin_user = Usuario(
                username="admin",
                email="admin@imobiliaria.com",
                senha_hash=senha_criptografada,
                funcao="Admin",
            )

            db.session.add(admin_user)
            db.session.commit()
            print("Usuário Admin (admin/123456) criado com sucesso!")

        # OBTÉM o objeto admin_user, caso já exista ou tenha sido criado agora.
        # Isso garante que temos o ID do Admin (que é 1 se for o primeiro usuário)
        if not admin_user:
            admin_user = Usuario.query.filter_by(username="admin").first()

        # ATENÇÃO: Se o Admin não for encontrado por algum motivo, definimos 1 como padrão
        admin_id = admin_user.id if admin_user else 1

        # 3. Verifica e insere imóveis de teste (se vazio)
        if Imovel.query.count() == 0:
            print("Nenhum imóvel encontrado. Inserindo dados de teste...")

            # ATRIBUI O ID DO ADMIN AO NOVO CAMPO 'usuario_id'
            imovel1 = Imovel(
                codigo="A101",
                cidade="Goiânia",
                bairro="Setor Bueno",
                tipo_imovel="Apartamento",
                quartos=3,
                vagas=2,
                banheiros=2,
                area_m2=95.5,
                valor=450000.00,
                status="Pronto",
                usuario_id=admin_id,  # <--- A CORREÇÃO!
            )

            imovel2 = Imovel(
                codigo="C050",
                cidade="Aparecida",
                bairro="Jardim Luz",
                tipo_imovel="Casa",
                quartos=2,
                vagas=1,
                banheiros=1,
                area_m2=70.0,
                valor=250000.00,
                status="Para Alugar",
                usuario_id=admin_id,  # <--- A CORREÇÃO!
            )

            imovel3 = Imovel(
                codigo="L202",
                cidade="Goiânia",
                bairro="Centro",
                tipo_imovel="Lote Comercial",
                quartos=0,
                vagas=0,
                banheiros=0,
                area_m2=300.0,
                valor=890000.00,
                status="Lançamento",
                usuario_id=admin_id,  # <--- A CORREÇÃO!
            )

            db.session.add_all([imovel1, imovel2, imovel3])
            db.session.commit()
            print("3 Imóveis de teste inseridos com sucesso!")

    app.run(debug=True)
