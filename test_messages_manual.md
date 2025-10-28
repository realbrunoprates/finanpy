# Guia de Teste Manual - Sistema de Mensagens Finanpy

## Informações de Acesso
- **URL Base**: http://localhost:8000
- **Email de Teste**: qa.tester@finanpy.com
- **Senha de Teste**: TestPass123!

## Objetivos dos Testes

1. Verificar se as mensagens aparecem corretamente em todas as views
2. Validar cores para cada tipo (SUCCESS=verde, ERROR=vermelho, WARNING=amarelo, INFO=azul)
3. Testar botão de fechar manual
4. Testar auto-dismiss após 5 segundos
5. Verificar animações (slide in e fade out)
6. Testar responsividade (mobile, tablet, desktop)
7. Verificar integração com design system

---

## Seção 1: Testes de Autenticação (users/)

### Teste 1.1: Login com Sucesso
**Requisito**: Mensagem SUCCESS "Bem-vindo de volta!"
**Passos**:
1. Acessar: http://localhost:8000/login/
2. Preencher email: qa.tester@finanpy.com
3. Preencher senha: TestPass123!
4. Clicar em "Entrar"

**Validações**:
- [ ] Mensagem aparece no topo direito
- [ ] Background: verde com transparência (bg-success/10)
- [ ] Border: verde com transparência (border-success/20)
- [ ] Texto em verde (#10b981)
- [ ] Ícone de checkmark circular visível
- [ ] Animação slide in da direita (300ms)
- [ ] Mensagem desaparece após 5 segundos automaticamente
- [ ] Posição: Fixed top-20 right-4

### Teste 1.2: Login com Erro
**Requisito**: Erro de validação no formulário
**Passos**:
1. Acessar: http://localhost:8000/login/
2. Preencher email: wrong@email.com
3. Preencher senha: wrongpass
4. Clicar em "Entrar"

**Validações**:
- [ ] Mensagem de erro no formulário (não é Django message)
- [ ] Texto: "E-mail ou senha inválidos."

### Teste 1.3: Logout com Sucesso
**Requisito**: Mensagem SUCCESS "Você saiu com sucesso."
**Passos**:
1. Estar logado
2. Clicar no botão "Sair" no navbar
3. Confirmar logout

**Validações**:
- [ ] Mensagem SUCCESS aparece
- [ ] Cores corretas (verde)
- [ ] Redirecionamento para login
- [ ] Mensagem visível após redirecionamento
- [ ] Posição: Fixed top-4 right-4 (usuário não autenticado)

### Teste 1.4: Signup com Sucesso
**Requisito**: Mensagem SUCCESS "Conta criada com sucesso! Bem-vindo ao Finanpy."
**Passos**:
1. Acessar: http://localhost:8000/signup/
2. Preencher nome: Novo Usuário
3. Preencher email: novo.usuario@test.com
4. Preencher senha e confirmação: NewPass123!
5. Clicar em "Cadastrar"

**Validações**:
- [ ] Mensagem SUCCESS aparece
- [ ] Login automático realizado
- [ ] Redirecionamento para dashboard
- [ ] Mensagem visível no dashboard

---

## Seção 2: Testes de Contas (accounts/)

### Teste 2.1: Criar Conta com Sucesso
**Requisito**: Mensagem SUCCESS "Conta criada com sucesso!"
**Passos**:
1. Login: qa.tester@finanpy.com
2. Acessar: http://localhost:8000/accounts/
3. Clicar em "Nova Conta"
4. Preencher nome: Conta de Testes QA
5. Selecionar tipo: Conta Corrente
6. Preencher saldo inicial: 5000.00
7. Clicar em "Salvar"

**Validações**:
- [ ] Mensagem SUCCESS aparece
- [ ] Cores corretas (verde #10b981)
- [ ] Redirecionamento para lista de contas
- [ ] Nova conta aparece na lista

### Teste 2.2: Atualizar Conta com Sucesso
**Requisito**: Mensagem SUCCESS "Conta atualizada com sucesso!"
**Passos**:
1. Acessar: http://localhost:8000/accounts/
2. Clicar em "Editar" em qualquer conta
3. Alterar nome: Conta Editada QA
4. Clicar em "Salvar"

**Validações**:
- [ ] Mensagem SUCCESS aparece
- [ ] Nome da conta atualizado na lista

### Teste 2.3: Excluir Conta com Sucesso
**Requisito**: Mensagem SUCCESS "Conta excluída com sucesso!"
**Passos**:
1. Acessar: http://localhost:8000/accounts/
2. Clicar em "Excluir" em qualquer conta
3. Confirmar exclusão

**Validações**:
- [ ] Mensagem SUCCESS aparece
- [ ] Conta removida da lista

---

## Seção 3: Testes de Categorias (categories/)

### Teste 3.1: Criar Categoria com Sucesso
**Requisito**: Mensagem SUCCESS "Categoria criada com sucesso!"
**Passos**:
1. Acessar: http://localhost:8000/categories/
2. Clicar em "Nova Categoria"
3. Preencher nome: Transporte QA
4. Selecionar tipo: Despesa
5. Clicar em "Salvar"

**Validações**:
- [ ] Mensagem SUCCESS aparece
- [ ] Nova categoria na lista de despesas

### Teste 3.2: Criar Categoria Duplicada (Erro)
**Requisito**: Erro de validação no formulário
**Passos**:
1. Acessar: http://localhost:8000/categories/
2. Clicar em "Nova Categoria"
3. Preencher nome de categoria existente
4. Clicar em "Salvar"

**Validações**:
- [ ] Mensagem de erro no formulário (não Django message)
- [ ] Texto: "Você já possui uma categoria com este nome."

### Teste 3.3: Atualizar Categoria com Sucesso
**Requisito**: Mensagem SUCCESS "Categoria atualizada com sucesso!"
**Passos**:
1. Acessar: http://localhost:8000/categories/
2. Clicar em "Editar" em qualquer categoria
3. Alterar nome: Categoria Editada QA
4. Clicar em "Salvar"

**Validações**:
- [ ] Mensagem SUCCESS aparece
- [ ] Nome da categoria atualizado

### Teste 3.4: Excluir Categoria com Sucesso
**Requisito**: Mensagem SUCCESS "Categoria excluída com sucesso!"
**Passos**:
1. Acessar: http://localhost:8000/categories/
2. Clicar em "Excluir" em categoria sem transações
3. Confirmar exclusão

**Validações**:
- [ ] Mensagem SUCCESS aparece
- [ ] Categoria removida da lista

---

## Seção 4: Testes de Transações (transactions/)

### Teste 4.1: Criar Transação de Receita com Sucesso
**Requisito**: Mensagem SUCCESS "Transação de receita criada com sucesso! O saldo da conta foi atualizado automaticamente."
**Passos**:
1. Acessar: http://localhost:8000/transactions/
2. Clicar em "Nova Transação"
3. Selecionar tipo: Receita
4. Preencher descrição: Salário de Teste
5. Preencher valor: 3000.00
6. Selecionar conta
7. Selecionar categoria de receita
8. Selecionar data
9. Clicar em "Salvar"

**Validações**:
- [ ] Mensagem SUCCESS aparece
- [ ] Texto menciona "receita"
- [ ] Transação aparece na lista

### Teste 4.2: Criar Transação de Despesa com Sucesso
**Requisito**: Mensagem SUCCESS "Transação de despesa criada com sucesso! O saldo da conta foi atualizado automaticamente."
**Passos**:
1. Clicar em "Nova Transação"
2. Selecionar tipo: Despesa
3. Preencher descrição: Compra de Teste
4. Preencher valor: 150.00
5. Selecionar conta
6. Selecionar categoria de despesa
7. Selecionar data
8. Clicar em "Salvar"

**Validações**:
- [ ] Mensagem SUCCESS aparece
- [ ] Texto menciona "despesa"

### Teste 4.3: Criar Transação com Erro de Validação
**Requisito**: Mensagem ERROR "Erro ao criar transação. Por favor, verifique os campos e tente novamente."
**Passos**:
1. Clicar em "Nova Transação"
2. Selecionar tipo: Receita
3. Selecionar categoria de DESPESA (erro de validação)
4. Preencher outros campos
5. Clicar em "Salvar"

**Validações**:
- [ ] Mensagem ERROR aparece
- [ ] Background: vermelho com transparência (bg-error/10)
- [ ] Border: vermelho com transparência (border-error/20)
- [ ] Texto em vermelho (#ef4444)
- [ ] Ícone de X circular visível
- [ ] Animação slide in da direita

### Teste 4.4: Atualizar Transação com Sucesso
**Requisito**: Mensagem SUCCESS "Transação atualizada com sucesso!"
**Passos**:
1. Acessar lista de transações
2. Clicar em "Editar" em qualquer transação
3. Alterar descrição
4. Clicar em "Salvar"

**Validações**:
- [ ] Mensagem SUCCESS aparece

### Teste 4.5: Atualizar Transação com Erro
**Requisito**: Mensagem ERROR "Erro ao atualizar transação. Por favor, verifique os campos e tente novamente."
**Passos**:
1. Editar transação
2. Alterar tipo de Receita para Despesa mas manter categoria de receita
3. Clicar em "Salvar"

**Validações**:
- [ ] Mensagem ERROR aparece
- [ ] Cores corretas (vermelho)

### Teste 4.6: Excluir Transação com Sucesso
**Requisito**: Mensagem SUCCESS "Transação excluída com sucesso!"
**Passos**:
1. Acessar lista de transações
2. Clicar em "Excluir" em qualquer transação
3. Confirmar exclusão

**Validações**:
- [ ] Mensagem SUCCESS aparece
- [ ] Transação removida da lista

---

## Seção 5: Testes de Perfil (profiles/)

### Teste 5.1: Atualizar Perfil com Sucesso
**Requisito**: Mensagem SUCCESS "Perfil atualizado com sucesso!"
**Passos**:
1. Acessar perfil do usuário
2. Clicar em "Editar Perfil"
3. Alterar campos (telefone, bio, etc)
4. Clicar em "Salvar"

**Validações**:
- [ ] Mensagem SUCCESS aparece
- [ ] Dados atualizados no perfil

---

## Seção 6: Testes de Design e UX

### Teste 6.1: Validação de Cores do Design System

**Para mensagem SUCCESS**:
- [ ] Background: rgba(16, 185, 129, 0.1) - verde com 10% opacidade
- [ ] Border: rgba(16, 185, 129, 0.2) - verde com 20% opacidade
- [ ] Texto: #10b981 (verde)
- [ ] Ícone: checkmark circular preenchido

**Para mensagem ERROR**:
- [ ] Background: rgba(239, 68, 68, 0.1) - vermelho com 10% opacidade
- [ ] Border: rgba(239, 68, 68, 0.2) - vermelho com 20% opacidade
- [ ] Texto: #ef4444 (vermelho)
- [ ] Ícone: X circular preenchido

**Para mensagem WARNING**:
- [ ] Background: rgba(245, 158, 11, 0.1) - amarelo com 10% opacidade
- [ ] Border: rgba(245, 158, 11, 0.2) - amarelo com 20% opacidade
- [ ] Texto: #f59e0b (amarelo/laranja)
- [ ] Ícone: triângulo de alerta

**Para mensagem INFO**:
- [ ] Background: rgba(59, 130, 246, 0.1) - azul com 10% opacidade
- [ ] Border: rgba(59, 130, 246, 0.2) - azul com 20% opacidade
- [ ] Texto: #3b82f6 (azul)
- [ ] Ícone: círculo com "i"

### Teste 6.2: Botão de Fechar Manual
**Passos**:
1. Gerar qualquer mensagem
2. Clicar no botão X (close) antes dos 5 segundos

**Validações**:
- [ ] Botão X visível no canto superior direito da mensagem
- [ ] Opacidade do botão: 70% normal, 100% ao hover
- [ ] Transição de opacidade suave (200ms)
- [ ] Ao clicar, mensagem é removida instantaneamente
- [ ] Sem animação de fade out ao fechar manual

### Teste 6.3: Auto-dismiss após 5 segundos
**Passos**:
1. Gerar qualquer mensagem
2. NÃO interagir com ela
3. Aguardar 5 segundos

**Validações**:
- [ ] Mensagem permanece visível por ~5 segundos
- [ ] Após 5 segundos, inicia animação de fade out
- [ ] Animação: opacity 0 + translateX(100%)
- [ ] Duração da animação: 500ms
- [ ] Mensagem removida do DOM após animação

### Teste 6.4: Animação Slide In
**Passos**:
1. Gerar qualquer mensagem
2. Observar entrada da mensagem

**Validações**:
- [ ] Animação começa fora da tela (translateX(100%))
- [ ] Slide da direita para esquerda
- [ ] Duração: 300ms
- [ ] Easing: ease-out
- [ ] Opacity vai de 0 para 1 simultaneamente

---

## Seção 7: Testes de Responsividade

### Teste 7.1: Mobile (375px × 667px)
**Passos**:
1. Redimensionar navegador ou usar DevTools
2. Gerar mensagens de diferentes tipos

**Validações**:
- [ ] Mensagens posicionadas em top-4 right-4 (quando não autenticado)
- [ ] Mensagens posicionadas em top-20 right-4 (quando autenticado)
- [ ] max-width: 384px (max-w-md)
- [ ] Mensagem não ultrapassa limites da tela
- [ ] Padding adequado (p-4)
- [ ] Texto legível, sem quebra inadequada
- [ ] Botão X acessível com toque
- [ ] Ícone visível e proporcional

### Teste 7.2: Tablet (768px × 1024px)
**Passos**:
1. Redimensionar para tablet
2. Gerar mensagens

**Validações**:
- [ ] Posicionamento consistente (top-20/top-4, right-4)
- [ ] Largura máxima respeitada
- [ ] Espaçamento adequado
- [ ] Todos os elementos visíveis

### Teste 7.3: Desktop (1920px × 1080px)
**Passos**:
1. Redimensionar para desktop
2. Gerar mensagens

**Validações**:
- [ ] Mensagens não ficam muito longe do canto
- [ ] max-w-md impede que fiquem muito largas
- [ ] Posicionamento fixed mantido
- [ ] Z-index 50 garante que ficam sobre outros elementos

### Teste 7.4: Múltiplas Mensagens
**Passos**:
1. Gerar múltiplas mensagens rapidamente (criar várias contas seguidas)

**Validações**:
- [ ] Mensagens empilham verticalmente
- [ ] Espaçamento entre mensagens: space-y-3
- [ ] Todas as mensagens visíveis
- [ ] Scroll funciona se necessário
- [ ] Auto-dismiss funciona para todas

---

## Seção 8: Testes de Integração com Design System

### Teste 8.1: Consistência Visual
**Validações**:
- [ ] Font-family: Inter (mesma do resto do app)
- [ ] Border-radius: rounded-lg
- [ ] Shadow: shadow-lg
- [ ] Backdrop blur: backdrop-blur-sm
- [ ] Transições: 200ms para hover do botão close
- [ ] Tema escuro: mensagens se destacam sobre bg-primary (#0f172a)

### Teste 8.2: Acessibilidade
**Validações**:
- [ ] role='alert' presente em cada mensagem
- [ ] Contraste de cores adequado (texto vs background)
- [ ] Ícones têm tamanho mínimo de 20px (w-5 h-5)
- [ ] Botão close tem área de toque adequada
- [ ] Mensagens podem ser lidas por screen readers

---

## Seção 9: Testes de Casos Especiais

### Teste 9.1: Mensagem Muito Longa
**Passos**:
1. Criar transação com descrição de 500 caracteres
2. Observar mensagem

**Validações**:
- [ ] Mensagem quebra texto adequadamente
- [ ] max-w-md impede overflow horizontal
- [ ] Mensagem cresce verticalmente
- [ ] Botão X permanece alinhado ao topo

### Teste 9.2: Navegação Rápida
**Passos**:
1. Criar conta (mensagem aparece)
2. Imediatamente navegar para outra página

**Validações**:
- [ ] Mensagem desaparece ao mudar de página
- [ ] Não há mensagens duplicadas
- [ ] Não há erro no console

### Teste 9.3: Mensagens em Página Sem Navbar
**Passos**:
1. Fazer logout (usuário não autenticado)
2. Acessar página de login
3. Observar posicionamento de mensagens

**Validações**:
- [ ] Mensagem usa top-4 (não top-20)
- [ ] Posicionamento adequado sem navbar

---

## Checklist Final de Validação

### Funcionalidade
- [ ] Todas as mensagens de sucesso aparecem corretamente
- [ ] Todas as mensagens de erro aparecem corretamente
- [ ] Auto-dismiss funciona consistentemente
- [ ] Botão manual de fechar funciona
- [ ] Múltiplas mensagens são gerenciadas corretamente

### Design System
- [ ] Cores SUCCESS (#10b981) aplicadas corretamente
- [ ] Cores ERROR (#ef4444) aplicadas corretamente
- [ ] Cores WARNING (#f59e0b) aplicadas corretamente
- [ ] Cores INFO (#3b82f6) aplicadas corretamente
- [ ] Transparências corretas (10% bg, 20% border)
- [ ] Ícones apropriados para cada tipo

### Animações
- [ ] Slide in (300ms, ease-out) funciona
- [ ] Fade out (500ms) funciona no auto-dismiss
- [ ] Transição do botão close (200ms) funciona

### Responsividade
- [ ] Mobile (320px+): Mensagens acessíveis e legíveis
- [ ] Tablet (768px+): Posicionamento correto
- [ ] Desktop (1024px+): Largura máxima respeitada

### Acessibilidade
- [ ] role='alert' presente
- [ ] Contraste adequado
- [ ] Área de toque mínima no botão close
- [ ] Leitura por screen readers possível

---

## Resultado Esperado

**Status Geral**: ✅ APROVADO | ❌ REPROVADO | ⚠️ APROVADO COM RESSALVAS

**Critérios para Aprovação**:
- Todos os testes funcionais devem PASSAR (100%)
- Cores do design system devem estar corretas (100%)
- Animações devem funcionar suavemente
- Responsividade deve funcionar em todos os tamanhos
- Acessibilidade básica deve estar presente

**Critérios para Reprovação**:
- Mensagens não aparecem em views críticas (login, CRUD operations)
- Cores incorretas (afeta UX e branding)
- Auto-dismiss não funciona
- Mensagens ilegíveis em mobile
- Erros no console do navegador
