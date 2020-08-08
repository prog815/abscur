import numpy as np
import pandas as pd

class ListGenetic:
    """
    Класс генетической оптимизации для списочных параметров

    Аргументы конструктора:
        pop_size - размер популяции
        mutate_koef - коэффициент мутации
        quality_method - метод расчета качества
        diaps - перечисление параметров со списками значений
    """
    _pop = None
    _diaps = None
    _quality = None
    _hist = None
    _mutate_koef = None
    _quality_method = None

    def __init__(self,pop_size=100,mutate_koef=0.01,quality_method=None,**diaps):
        """
        
        """
        import numpy as np
        
        self._diaps = diaps
        assert len(diaps) > 0 , "Нет параметров для генетической оптимизации"
        self._pop = np.random.rand(pop_size,len(diaps))
        self._quality = np.zeros((pop_size,))-float('inf')
        self._hist = []
        self._mutate_koef = mutate_koef
        self._quality_method = quality_method
        
    def fit(self,epochs=10):
        """
        Запуск генетической оптимизации.

        Аргументы:
            epochs - кол-во эпох оптимизации
        """
        import numpy as np
        
        for ep in range(epochs):
            # генерация нового
            new = self._new_genom()

            # расчет качества
            q = self._get_quality(new)

            # замена старого
            n = len(self._hist) % len(self._pop)
            self._pop[n,:] = new
            self._quality[n] = q
            
            # запись истории
            hist_new = { "quality" : q }
            hist_new.update(self._get_gen_params(new))
            
            hist = {"new" : hist_new}

            self._hist.append(hist)

            print(len(self._hist),hist_new)
    
    def _new_genom(self):
        import numpy as np
        
        idxSorted = np.argsort(self._quality)
        idx1,idx2 = np.random.choice(idxSorted[np.round(len(idxSorted))//2:],size=2,replace=False)
        new_genom = self._xver(self._pop[idx1],self._pop[idx2])
        new_genom = self._mutate(new_genom)
        return new_genom

    def _get_quality(self,genom):
        params = self._get_gen_params(genom)
        return self._quality_method(**params)
        

    def _get_gen_params(self,genom):
        import numpy as np

        param_list = list(self._diaps.keys())
        
        def gen2par(g,par_list):
            N = len(par_list)
            idx = int(np.clip(np.round(g*N-0.5),0,N-1))
            return par_list[idx]

        return {key : gen2par(g,self._diaps[key]) for key,g in zip(param_list,genom)}
        
    def _xver(self,genom1,genom2):
        import numpy as np

        new_genom = np.array(genom1)
        for i in range(len(new_genom)):
            if np.random.randn() > 0:
                new_genom[i] = genom1[i]
            else:
                new_genom[i] = genom2[i]
        return new_genom

    def _mutate(self,genom):
        import numpy as np

        new_genom = genom + np.random.randn(len(genom))*self._mutate_koef
        new_genom = np.clip(new_genom,0.,1.)
        return new_genom

    def plot_hist_new(self,params=('quality',)):
        """
        Вывод истории оптимизации

        Аргументы:
            params - список параметров для вывода
        """
        import matplotlib.pyplot as plt
        import numpy as np
        
        def getQM(data,N=20):
            L = len(data)
            dN = L//N
            gl = L//10
            x = list(range(dN,L,dN))
            if x[-1] != L-1:
                x.append(L-1)
            q1 = np.array(x,dtype=float)
            m = np.array(x,dtype=float)
            q2 = np.array(x,dtype=float)
            for i in range(len(x)):
                q1[i],m[i],q2[i] = np.quantile(data[(max(0,x[i]-gl)):(x[i]+1)],(0.1,0.5,0.9))
            return x,q1,m,q2

        for param in params:
            plt.figure(figsize=(10,6))
            v = [h['new'][param] for h in self._hist]
            plt.plot(v,'y.',label='<'+param+'>')
            x,q1,m,q2 = getQM(v)
            plt.plot(x,q2,':',label='q2')
            plt.plot(x,m,'*k-',label='m')
            plt.plot(x,q1,':',label='q1')
            plt.title('параметр <' + param + '>')
            plt.legend()
            plt.show()
    
    def getBestParams(self,method='pop_mean',**kwargs):
        """
        Выдача лучших параметров

        Аргументы:
            method - метод извлечения
                варианты:
                - pop_mean - среднее по популяции
                - pop_q - серединный квантиль по популяции
                
        """
        import numpy as np

        params = list(self._diaps.keys())

        if method == 'pop_mean':
            return self._get_gen_params(self._pop.mean(axis=0))
        
        if method == 'pop_q':
            return self._get_gen_params(np.quantile( m._pop,0.5,axis=0))

        raise Exception('неверный метод')



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
