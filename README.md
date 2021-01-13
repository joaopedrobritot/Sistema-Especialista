<h2 align="center"> Projeto IA - Sistema Especialista para Recomendação de Notebooks </h2>

<p align="center"><a href="https://ufal.br" target="_blank"><img src="/img/uf.png" width="400"></a></p>

Instalação:

- Baixa os arquivos desse repositório.
- Instale as dependências utilizando o pip, na raiz do projeto:
```cmd 
    pip install requirements.txt
```

Opções de uso:

- Modo terminal
```cmd
    python main.py input.txt
```
obs. Caso deseje testar o modo de interface, que não está concluido, utilize o argumento -m [interface]

Funcionamento:

- Ao iniciar o bot:

<img src="/img/inicio_.png" width="800">

- Utilizando o bot e chegando a uma resposta:

<img src="/img/img_2.png" width="800">

- Resposta final do bot:

<img src="/img/img_3.png" width="800">

- Modo interface (em testes, desconsidere para avaliação):

<img src="/img/img_4.png" width="400">

- Utilização do algoritmo de backward chaining:

```python
    def solve(self):
        if self.visited is True:
            return self.state

        state = None
        if self.state is not None:
            state = self.state
            if self.state_fixed is True:
                return state
        fixed_ret = []
        unfixed_ret = []

        f, u = self.solve_grouped_nodes(self.children, False)
        fixed_ret.extend(f)
        unfixed_ret.extend(u)

        self.solve_grouped_nodes(self.operand_parents, True)

        ret = fixed_ret if fixed_ret.__len__() is not 0 else unfixed_ret
        if ret.__len__() is not 0:
            if True in ret:
                state = True
            else:
                state = False

        is_fixed = True if fixed_ret.__len__() is not 0 else False

        need_reverse = True
        if state is None:
            need_reverse = False
            state = self.state

        if state is not None:
            if isinstance(self, NegativeNode) and need_reverse:
                state = not state if state is not None else None
            return self.set_state(state, is_fixed)
        return None
```

<a href='https://www.kaggle.com/ghadahalshehrei/laptops-info' target="_blank">- Base de dados</a>

<a href='https://drive.google.com/file/d/1WFREfKPIi2XKRzFq3tIXRyPSZfzlRMbR/view?usp=sharing' target="_blank">- Diagrama de Árvore</a>

<a href='/dictionaries/notebooks.txt' target="_blank">- Lista de Notebooks Inclusos</a>

<a href='/input.txt' target="_blank">- Arquivo Inicial de Regras</a>
