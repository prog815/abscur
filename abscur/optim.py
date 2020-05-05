import numpy as np
import pandas as pd

class GenomOptim():
    """
    Класс генетической оптимизации
    Пытаемся найти параметры минимума функции

    """

    def __init__(self,par_dict_vls,score_fnc,pop_len=100,mu=0.01,kill_second_parent=False):
        """
        Инициализация класса
        
        Параметры:
        par_dict_vls - словарь параметров целевой функции
        score_fnc - целевая функция
        pop_len - размер популяции
        mu - коэффициент мутации
        kill_second_parent - нужно ли убивать второго родителя

        Свойства:
        hist - история оптимизации (Pandas.DataFrame)
            первые поля - параметры целевой функции
            new_score - качество нового элемента
            mean_score - среднее качество по популяции
            std_score - дисперсия по популяции

        """

        # параметры оптимизации
        self.par_dict_vls = par_dict_vls

        # функция для оптимизации возвращающая качество
        self.score_fnc = score_fnc

        # создаем популяцию
        self.pop = np.random.rand(pop_len,len(par_dict_vls)) 

        # качество элементов популяции
        self.pop_q = np.array([np.inf]*self.pop.shape[1])

        # История оптимизации
        self.hist = pd.DataFrame(columns=list(par_dict_vls.keys())+['new_score','mean_score','std_score'])
        
        # коэффициент мутации
        self.mu = mu

        # убивать второго родителя?
        self.kill_second_parent = kill_second_parent

    def step(self):
        """
        Один шаг оптимизации
        """
        # делим популяцию на две выборки по качеству
        ind_pop = np.argsort(self.pop_q)
        ind_pop_good = ind_pop[:len(ind_pop)//2]
        ind_pop_bad = ind_pop[len(ind_pop)//2:]

        # отбираем родителей для скрещивания и место в плохой половине популяции
        ind_g0,ind_g1 = np.random.choice(ind_pop_good,2)
        ind_b = np.random.choice(ind_pop_bad)

        # скрещивание 
        self.pop[ind_b,:] = self.pop[ind_g0,:]
        gen_len = self.pop.shape[1]
        ind = np.random.choice(list(range(gen_len)),gen_len//2)
        self.pop[ind_b,ind] = self.pop[ind_g1,ind]

        # мутация
        self.pop[ind_b,:] += np.random.randn(gen_len)*self.mu
        self.pop[ind_b,:] = np.clip(self.pop[ind_b,:],0,1)

        # извлекаем параметры из генома
        new_par_dict = {}
        par_names = list(self.par_dict_vls.keys())
        for i in range(len(par_names)):
            gpn = par_names[i]
            gp_len = len(self.par_dict_vls[gpn])
            new_par_dict[gpn] = self.par_dict_vls[gpn][min(int(self.pop[ind_b,i]*gp_len),gp_len-1)]
        
        # считаем новое качество
        self.pop_q[ind_b] = self.score_fnc(**new_par_dict)

        # убиваем (снижаем качество) второго родителя
        if self.kill_second_parent:
            self.pop_q[ind_g1] = np.median(self.pop_q)
        
        # фиксируем изменения в истоии
        new_par_dict['new_score'] = self.pop_q[ind_b]
        new_par_dict['mean_score'] = np.mean(self.pop_q[np.isfinite(self.pop_q)])
        new_par_dict['std_score'] = np.std(self.pop_q[np.isfinite(self.pop_q)])

        #print(new_par_dict)
        self.hist = self.hist.append(new_par_dict,ignore_index=True)
