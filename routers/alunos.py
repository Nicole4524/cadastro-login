@router.post("/cadastro", response_model=AlunoResponse, status_code=201, summary="Cadastrar aluno")
def cadastrar_aluno(body: AlunoCreate, db: Session = Depends(get_db)):
    try:
        print("\n================ CADASTRO ALUNO ================")
        print("BODY RECEBIDO:", body)

        print("Nome:", repr(body.nome))
        print("Email:", repr(body.email))
        print("Telefone:", repr(body.telefone))
        print("CPF:", repr(body.cpf))
        print("Matricula:", repr(body.matricula))

        print("Senha:", repr(body.senha))
        print("Tipo da senha:", type(body.senha))
        print("Tamanho da senha:", len(body.senha))
        print("================================================\n")

        if db.query(Aluno).filter(Aluno.email == body.email).first():
            raise HTTPException(status_code=400, detail="E-mail já cadastrado")

        if db.query(Aluno).filter(Aluno.matricula == body.matricula).first():
            raise HTTPException(status_code=400, detail="Matrícula já cadastrada")

        if db.query(Aluno).filter(Aluno.cpf == body.cpf).first():
            raise HTTPException(status_code=400, detail="CPF já cadastrado")

        if body.motorista_id:
            if not db.query(Motorista).filter(Motorista.id == body.motorista_id).first():
                raise HTTPException(status_code=404, detail="Motorista não encontrado")

        print("Gerando hash da senha...")

        senha_hash = hash_password(body.senha)

        print("Hash gerado com sucesso!")
        print("Tamanho do hash:", len(senha_hash))

        aluno = Aluno(
            nome=body.nome,
            email=body.email,
            telefone=body.telefone,
            senha_hash=senha_hash,
            cpf=body.cpf,
            matricula=body.matricula,
            escola=body.escola,
            endereco=body.endereco,
            cidade=body.cidade,
            estado=body.estado,
            cep=body.cep,
            motorista_id=body.motorista_id,
        )

        print("Adicionando aluno ao banco...")

        db.add(aluno)

        print("Executando commit...")

        db.commit()

        print("Commit realizado com sucesso!")

        db.refresh(aluno)

        print("Aluno criado com ID:", aluno.id)

        return aluno

    except Exception as e:
        import traceback

        print("\n================ ERRO CADASTRO ================")
        print("TIPO:", type(e)._name_)
        print("ERRO:", str(e))
        print("TRACEBACK COMPLETO:")
        traceback.print_exc()
        print("================================================\n")

        raise
