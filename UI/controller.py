import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYears(self):
        try:
            anno1 = self._model.getAllYears()
            for y in anno1:
                self._view._ddAnno1.options.append(ft.dropdown.Option(y))
                # key=actor.id,
                #  text=actor.name))
           # self._view.update_page()

        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore nel recupero del primo anno: {ex}", color="red"))

        try:
            anno2 = self._model.getAllYears()
            for y in anno2:
                self._view._ddAnno2.options.append(ft.dropdown.Option(y))
                # key=actor.id,
                #  text=actor.name))
            self._view.update_page()

        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore nel recupero del secondo anno: {ex}", color="red"))
        self._view.update_page()


    def handleCreaGrafo(self,e):
        anno1 = self._view._ddAnno1.value
        anno2 = self._view._ddAnno2.value
        if not anno1:
            self._view.create_alert("Selezionare la prima data prima di creare il grafo.", color="red")
            return
        if not anno2:
            self._view.create_alert("Selezionare la seconda data prima di creare il grafo.", color="red")
            return

        try:
            self._model.creaGrafo(anno1, anno2)
            n_nodes = self._model.get_num_nodes()
            n_edges = self._model.get_num_edges()
            # Stampa immediata numero di vertici e archi (Punto 1.c)
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Grafo creato con successo!\nNumero vertici: {n_nodes}\nNumero archi: {n_edges}",
                        color="green"))
            # RIEMPIO IL DROPDOWN DEI FILM DEL GRAFO
            #self.fillDDArtisti()

        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore durante la creazione del grafo: {ex}", color="red"))
            # return
        self._view.update_page()

    def handleDettagli(self, e):
        numero, largest, details = self._model.getConnessaInfo()
        self._view._txt_result.controls.clear()

        # C) 3 ARCHI CON PESO MAGGIORE
        top3 = self._model.getTop3Archi()
        # self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f" 3 Archi di peso maggiore ", color="green"))

        # self._view._txt_result.controls.append(ft.Text(f"{arco[0]}-->{arco[1]} (peso: {arco[2]["weight"]})"))
        for i, arco in enumerate(top3, start=1):
            a1, a2, dati = arco
            self._view._txt_result.controls.append( ft.Text(
                    f"{i})  {a1.name}  ({a1.constructorId}) -- {a2.name}  ({a2.constructorId} )"
                    f"(piloti condivisi: {dati['weight']})")
            )

        #self._view._txt_result.controls.append(
          #  ft.Text(f"Il grafo contiene {numero} componenti connesse\n", color="green"))
       # self._view._txt_result.controls.append(
           # ft.Text(f"Film con maggior numero archi uscenti: {film_max_out} (archi uscenti: {max_out})\n", color="green"))
        self._view._txt_result.controls.append(
            ft.Text(f"Il grafo ha  {numero} componenti connesse\n", color="orange"))

        self._view._txt_result.controls.append(
            ft.Text(f"La componente connessa maggiore ha dimensione  {len(largest)}\n", color="green"))

        for titolo in largest:
            self._view._txt_result.controls.append(ft.Text(f"{titolo} "))

        self._view._txt_result.controls.append(
            ft.Text(f"La componente connessa maggiore in ordine decrescente \n", color="green"))

        for titolo, numero_piloti in details:
            self._view._txt_result.controls.append(ft.Text(f"{titolo}: {numero_piloti} piloti"))
            
        self._view.update_page()

    def handleCerca(self, e):
        self._view._txt_result.controls.clear()

        if self._model.get_num_nodes() == 0 or self._model.get_num_edges() is None:
            self._view.create_alert("Creare prima il grafo!", color="red")
            return
        k = self._view._txtInK.value
        # qui dovremmo fare i solti controlli sulla validità

        try:
            kInt = int(k)
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore ! devi inserire un intero per procedere: {ex}", color="red")
            )
            self._view.update_page()
            return
        if kInt <= 0:
            self._view.create_alert(
                "N deve essere un intero positivo.", color="red")
            return

        gruppo, scarto = self._model.getGruppoPiloti(kInt)

        if len(gruppo) < kInt:
            self._view._txt_result.controls.append(
                ft.Text("Non esiste una selezione valida di K costruttori.") )
        else:
            self._view._txt_result.controls.append(
                ft.Text(f"Scarto minimo: {scarto} giorni")   )

            for costruttore in gruppo:
                self._view._txt_result.controls.append(
                    ft.Text(
                        f"{costruttore.name} - "
                        f"Veterano nato il {costruttore.oldest_driver_dob}" )
                )

            piu_anziano = min(  gruppo, key=lambda c: c.oldest_driver_dob )

            piu_giovane = max( gruppo, key=lambda c: c.oldest_driver_dob )

            self._view._txt_result.controls.append(
                ft.Text(f"Veterano più anziano: {piu_anziano.name}")  )

            self._view._txt_result.controls.append(
                ft.Text(f"Veterano più giovane: {piu_giovane.name}")   )

        self._view.update_page()



