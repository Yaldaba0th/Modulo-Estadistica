   """
        print(count[0])
        data = count[0]
        #Datos estadisticos(N° de arriendos por mes)
        
            #Arriendos por mes 
        prom = np.mean(data)
        print(prom)

            #meses mas visitado por año
        mesmax = self.months[np.argmax(data)]
        print(mesmax)
            #3 meses mas visitados por el año seleccionado
        argsmax = []
        for i in range(3):
            argmax = np.argmax(data)
            argsmax.append(argmax)
            data = np.delete(data, argmax)
        print(self.months[argsmax[0]])
        print(self.months[argsmax[1]])
        print(self.months[argsmax[2]])

        #Datos esatdisticos(N° personas por región)
        
        argmax = np.argmax(data)
        month =  self.region[argmax] # Region que se recibe mas visitas
        print(month)
        """