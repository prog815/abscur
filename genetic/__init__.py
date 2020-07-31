class ListGenetic:
    
    _pop = None
    _diaps = None
    _quality = None
    _hist = None
    _mutate_koef = None
    _quality_method = None

    def __init__(self,pop_size=100,mutate_koef=0.01,quality_method=None,**diaps):
        import numpy as np
        
        self._diaps = diaps
        assert len(diaps) > 0 , "Нет параметров для генетической оптимизации"
        self._pop = np.random.rand(pop_size,len(diaps))
        self._quality = np.zeros((pop_size,))-float('inf')
        self._hist = []
        self._mutate_koef = mutate_koef
        self._quality_method = quality_method
        
    def fit(self,epochs=10):
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
        import matplotlib.pyplot as plt
        import numpy as np
        
        for param in params:
            v = [h['new'][param] for h in self._hist]
            plt.plot(v)
            plt.title(param)
            plt.show()

