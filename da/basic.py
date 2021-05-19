from anytree import Node, RenderTree
import pandas as pd

osoby = 'Alex, Alfred, Anita, Anne, Bernard, Bill, Charles, Claire, David, Eric, Frans, George, Herman, Joe, Maria, Max, Paul, Peter, Philip, Richard, Robert, Sam, Susan, Tom'.split(', ')


df = pd.read_csv('da/pytania.csv')
nazwy = df[['nazwa', 'wartosc']]
zbior = df[osoby]

class Nd(Node):

    def __init__(self, name='root', d: pd.DataFrame = zbior.transpose(), parent=None, **kwargs):
        super().__init__(name, parent=parent, children=[], **kwargs)
        self.df = d
        

    def solve(self):
        print(len(self.df))
        if len(self.df) > 1:
            self.gen()
        elif len(self.df) == 1:
            print(f'person is {self.df.index[0]}')
            Node(f'person is {self.df.index[0]}', self)

    def gen(self):
        l = len(self.df)
        eff = self.df.sum().apply(lambda x: min((x,l-x))/max((x,l-x)))

        question_id = eff.idxmax()
        pytanie, odpowiedz = nazwy.loc[question_id]
        print('pytanie:', pytanie)

        answers = self.df[question_id]

        yes = self.df[answers == True].drop(columns=(question_id))
        Nd(f'{pytanie} is {odpowiedz}? yes', yes, self).solve()

        no = self.df[answers == False].drop(columns=(question_id))
        Nd(f'{pytanie} is {odpowiedz}? no', no, self).solve()

if __name__ == '__main__':
    solved = Nd()
    solved.solve()

    print()
    print()

    for pre, fill, node in RenderTree(solved):
        print("%s%s" % (pre, node.name))

    print()
    print()

    print('osoby:', len(solved.leaves))
    print('najdłużej:', max((i.depth for i in solved.leaves)))
    print('najkrócej:', min((i.depth for i in solved.leaves)))