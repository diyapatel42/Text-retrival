import tkinter
from tkinter import *
from tkinter.ttk import *
import numpy as np
import get_index
import search

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.ranker = None
        self.doc_dict = None

    def create_widgets(self):
        # window title
        self.winfo_toplevel().title("Search with BM25")
        # GUI lables
        self.l1 = tkinter.Label(self.master, text="A simple App for text retrieval", font=("Arial", 18))
        self.l2 = tkinter.Label(self.master, text="Search Query")
        self.scrollbar = Scrollbar(self.master, orient="vertical")

        # GUI (grid) locations

        self.l1.grid(row=0, column=1, sticky=W)
        self.l2.grid(row=1, column=0)

        # entry field
        # query input
        self.query_text = tkinter.Entry(self.master, width=80)

        # align the entries with the labels
        self.query_text.grid(row=1, column=1, sticky=W)  # left align

        # text area for display the result
        self.result = Text(self.master, width=60, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.result.yview)
        self.scrollbar.grid(row=4, column=2)
        self.result.grid(row=4, column=1, sticky=W)
        # GUI style
        self.style = tkinter.ttk.Style()
        # different conditions
        self.style.map('D.TButton', foreground=[('pressed', 'red'), ('active', 'green')],
                       background=[('pressed', '!disabled', 'black'), ('active', 'white')])
        self.index = tkinter.ttk.Button(self.master, text="Index", style="D.TButton")
        self.index.grid(row=5, column=0, sticky=W)

        self.index["command"] = self.index_document

        # button to rank the documents given the query
        self.search = Button(self.master, text="Search", style="D.TButton")
        self.search.grid(row=1, column=3, sticky=W)

        # click command of the "Search" button to the get_query function
        self.search["command"] = self.get_query

        self.quit = Button(self.master, text="Quit", style="D.TButton", command=self.master.destroy)
        self.quit.grid(row=5, column=2, sticky=E)

    def get_query(self):

        # get the query string from the query text box
        query = self.query_text.get()

        if self.ranker is None:
            self.result.insert(END, "Please index the documnents first. \n")
            return
        # query_process function from the search.py script to get the tokenized_query
        tokenized_query = search.query_process(query)
        self.result.insert(END, "\n" + "The query tokens: ")

        # insert the tokenized query terms to the "result" text field
        self.result.insert(END, tokenized_query)
        self.result.insert(END, "\n")

        # documents ranking scores by the get_scores method of the ranker object
        # the input of the get_scores function is the tokenized query terms
        doc_scores = self.ranker.get_scores(tokenized_query)

        # ranking results as a string by calling the show_ranking function
        rank_result = self.show_ranking(doc_scores, self.doc_dict)

        # formatted ranked top 5 documents and their score by calling the print_top5 function
        result = self.print_top5(rank_result)
        # insert the result formatted string to the result text field
        self.result.insert(END, result)

        self.result.insert(END, "\n")

    def index_document(self):
        """
        the function uses the build_ranker function from the get_index script to get the BM25 ranker
        and the document dict {doc_name:text}
        :return:
        it will set the ranker and the doc_doc_dict properties of the object
        """
        # call the build_ranker function from the get_index script
        # and return the BM25 ranker and the document dict
        bm25_ranker, document_dict = get_index.build_ranker()
        self.result.insert(END, "The document collection has been indexed. \n")
        # ranker and doc_dict properties, remember to add "self." in the front
        self.ranker = bm25_ranker
        self.doc_dict = document_dict

    def show_ranking(self, doc_scores, doc_dict):
        """
        :param doc_scores: the numpy array of document ranking scores
        :param doc_dict: the document dict {file_name: text}
        :return: a list of tuples, in a tuple (file_name, file_ranking_score}
        """
        doc_idx_dict = {}
        # argsort method from numpy to sort the score array ascendingly
        # reverse the order to descending, use the [::-1] method to numpy array
        sorted_idx = np.argsort(doc_scores)
        sorted_idx = sorted_idx[::-1]

        for i, doc_name in enumerate(doc_dict.keys()):
            doc_idx_dict[i] = doc_name

        ranking = []
        # the tuple (file_name, doc_score) to the ranking list
        # iterate the sorted_idx where the scores have been sorted descendingly
        # document name can get from the doc_dix_dict where the document names are numbered
        # the doc_score can get from the doc_scores by the corresponding index

        for position in sorted_idx:
            ranking.append((doc_idx_dict[position], doc_scores[position]))
        return ranking

    def print_top5(self, ranking):
        results = ""
        for i in range(5):
            # reformatted the string by the string "  ".format() method
            print_out = "document name -- {}, score -- {:.4f}".format(ranking[i][0], ranking[i][1])
            if i == 4:
                results = results + print_out
            else:
                results = results + print_out + "\n"

        return results


# launch the GUI
root = Tk()
root.geometry("800x600")
app = Application(master=root)
app.mainloop()
