# Agentes de IA - Finanpy

Esta pasta contém os agentes de IA especializados para desenvolvimento do Finanpy. Cada agente é especialista em uma área específica da stack tecnológica e segue rigorosamente os padrões definidos na documentação do projeto.

## Sobre os Agentes

Os agentes são prompts especializados que podem ser usados com Claude Code ou outros assistentes de IA para realizar tarefas específicas no projeto. Cada agente possui:

- **Expertise específica** na tecnologia da stack
- **Conhecimento profundo** da documentação do projeto
- **Acesso a ferramentas** via MCP servers quando aplicável
- **Responsabilidades claras** e bem definidas

## Stack do Projeto

- **Backend**: Python 3.13+ e Django 5+
- **Frontend**: Django Template Language + TailwindCSS
- **Banco de Dados**: SQLite3 (desenvolvimento)
- **Autenticação**: Django Auth nativo

## Agentes Disponíveis

### 1. Backend Developer
**Arquivo**: `backend-developer.md`

**Especialidade**: Python, Django, Models, Views, Business Logic

**Usa MCP**: `context7` (documentação Django/Python atualizada)

**Quando usar**:
- Criar ou modificar models Django
- Implementar views e lógica de negócio
- Configurar URLs e rotas
- Trabalhar com Django ORM e queries
- Implementar signals e managers
- Criar forms e validações
- Configurar Django Admin

**Exemplos de tarefas**:
- "Implementar o modelo Account com todos os campos do PRD"
- "Criar views CRUD para transações"
- "Adicionar validação de saldo ao criar transação de saída"
- "Implementar signal para atualizar saldo da conta automaticamente"

---

### 2. Frontend Developer
**Arquivo**: `frontend-developer.md`

**Especialidade**: Django Templates, HTML, TailwindCSS, JavaScript vanilla

**Usa MCP**: `context7` (documentação TailwindCSS e Django Templates)

**Quando usar**:
- Criar templates HTML com Django Template Language
- Implementar componentes de UI com TailwindCSS
- Trabalhar com formulários e validações no frontend
- Adicionar interatividade com JavaScript vanilla
- Garantir responsividade e acessibilidade
- Implementar o design system do projeto

**Exemplos de tarefas**:
- "Criar template do dashboard com cards de estatísticas"
- "Implementar formulário de cadastro de transação"
- "Criar componente de navbar seguindo o design system"
- "Adicionar validação de formulário no frontend com JavaScript"

---

### 3. QA Tester
**Arquivo**: `qa-tester.md`

**Especialidade**: Testes automatizados, validação de UI/UX, Playwright

**Usa MCP**: `playwright` (testes E2E e validação visual)

**Quando usar**:
- Validar funcionalidades implementadas
- Verificar se o design está correto
- Testar fluxos de usuário completos
- Validar responsividade
- Verificar acessibilidade básica
- Encontrar bugs e inconsistências
- Validar casos de uso do PRD

**Exemplos de tarefas**:
- "Testar o fluxo completo de criação de transação"
- "Validar se o dashboard exibe os dados corretos"
- "Verificar se as cores do design system estão sendo aplicadas"
- "Testar responsividade do formulário de conta"

---

### 4. Tech Lead
**Arquivo**: `tech-lead.md`

**Especialidade**: Arquitetura, Code Review, Best Practices, Decisões Técnicas

**Usa MCP**: `context7` (documentação de best practices)

**Quando usar**:
- Revisar código implementado
- Tomar decisões arquiteturais
- Planejar implementação de features complexas
- Resolver problemas de design de código
- Garantir aderência aos padrões do projeto
- Refatorar código existente
- Otimizar performance

**Exemplos de tarefas**:
- "Revisar implementação dos models de transação e conta"
- "Sugerir melhor arquitetura para cálculo de saldos"
- "Refatorar views para seguir DRY"
- "Planejar migração de SQLite para PostgreSQL"

---

## Como Usar os Agentes

### 1. Escolha o Agente Apropriado

Identifique a natureza da tarefa e escolha o agente especializado:
- **Backend**: Models, views, business logic, banco de dados
- **Frontend**: Templates, UI, estilos, interatividade
- **QA**: Testes, validação, verificação de requisitos
- **Tech Lead**: Arquitetura, review, planejamento, refatoração

### 2. Leia o Arquivo do Agente

Abra o arquivo `.md` do agente escolhido e copie o prompt completo.

### 3. Forneça Contexto

Ao usar o agente, sempre forneça:
- A tarefa específica a ser realizada
- Arquivos relevantes (use @ para referenciar)
- Requisitos do PRD relacionados (se aplicável)
- Padrões de design system (se aplicável)

### 4. Valide o Resultado

Após o agente completar a tarefa:
- **Backend**: Teste manualmente ou use o QA Tester
- **Frontend**: Visualize no navegador e use o QA Tester
- **Código em geral**: Considere usar o Tech Lead para review

## Exemplo de Workflow

### Feature: Implementar CRUD de Contas Bancárias

```
1. Tech Lead
   → Planejar arquitetura e fluxo de implementação
   → Definir estrutura de models, views e templates

2. Backend Developer
   → Implementar modelo Account
   → Criar views CRUD
   → Configurar URLs
   → Adicionar ao Django Admin

3. Frontend Developer
   → Criar templates de listagem
   → Criar formulário de cadastro/edição
   → Implementar página de detalhes
   → Aplicar design system

4. QA Tester
   → Testar CRUD completo
   → Validar design e responsividade
   → Verificar casos de uso do PRD
   → Reportar bugs encontrados

5. Tech Lead
   → Code review final
   → Aprovar ou solicitar ajustes
```

## Documentação Importante

Todos os agentes têm conhecimento de:

- **PRD.md**: Product Requirements Document completo
- **docs/setup.md**: Setup e instalação
- **docs/project-structure.md**: Estrutura de apps e pastas
- **docs/coding-standards.md**: Padrões de código obrigatórios
- **docs/architecture.md**: Arquitetura técnica e decisões
- **docs/design-system.md**: Sistema de design completo
- **CLAUDE.md**: Guia rápido para IA trabalhar no projeto

## MCP Servers Utilizados

### context7
Fornece acesso a documentação oficial atualizada de:
- Python
- Django (5.x)
- TailwindCSS
- HTML/CSS
- JavaScript

**Agentes que usam**: Backend Developer, Frontend Developer, Tech Lead

### playwright
Permite execução de testes automatizados E2E:
- Navegação no browser
- Validação de elementos
- Testes de interação
- Validação visual
- Screenshots

**Agentes que usam**: QA Tester

## Boas Práticas

### Ao Usar os Agentes

1. **Um agente por vez**: Não misture responsabilidades
2. **Forneça contexto completo**: Quanto mais contexto, melhor o resultado
3. **Valide o output**: Sempre revise o código gerado
4. **Use o workflow**: Tech Lead → Dev → QA → Tech Lead
5. **Documente mudanças**: Atualize docs se necessário

### Limitações

- Agentes não substituem revisão humana
- Sempre teste manualmente após implementação
- Use o Tech Lead para decisões arquiteturais importantes
- QA Tester é complementar a testes manuais

## Contribuindo com Novos Agentes

Se necessário criar novos agentes especializados:

1. Identifique a necessidade específica
2. Defina responsabilidades claras (sem overlap)
3. Liste a expertise técnica necessária
4. Defina quando usar o agente
5. Forneça exemplos de tarefas
6. Inclua conhecimento da documentação do projeto
7. Adicione ao README.md
