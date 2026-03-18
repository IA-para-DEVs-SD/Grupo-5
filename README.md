# 🚀 KiroSonar - Code Review e Auto-Fix com IA

O KiroSonar é uma CLI nativa em Python que atua como um "SonarQube tunado". Ele analisa o `git diff` do seu projeto, envia para a IA avaliar (identificando Bugs, Vulnerabilidades, Code Smells e Dívida Técnica) e aplica a refatoração automaticamente no seu código.

## 🛠️ Setup do Ambiente de Desenvolvimento

Nossa equipe utiliza o **Conda** para garantir que todos desenvolvam na mesma versão do Python (3.11), evitando quebras de ambiente.

### 1. Pré-requisitos
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) instalado na máquina.
- Binário `kiro-cli` configurado no PATH do seu sistema.

### 2. Configurando o Ambiente
No terminal, na raiz do projeto, execute os comandos abaixo para criar e ativar o ambiente isolado:

```bash
conda create -n kirosonar python=3.11 -y
conda activate kirosonar
```

### 3. Instalando a CLI (Modo Dev)
Para que o comando `kirosonar` funcione nativamente no terminal e reflita suas mudanças de código em tempo real, instale o pacote em modo de edição:

```bash
pip install -e .
```

## 📚 Documentação
Para entender a arquitetura, o fluxo do CLI e as regras de negócio, leia o nosso [RFC 001](./docs/RFC-001-KiroSonar-MVP.md).