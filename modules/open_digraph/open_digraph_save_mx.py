import os

class open_digraph_save_mx:
  def save_as_dot_file(self, path : str = "dot_files/open_digraph/graph.dot", verbose : bool = False) -> None :
    """
    Saves the graph in a dot file
    The verbose adds the id in the file, not only the label of a node
    The add argument says if we add the graph at the end of the file
    """
    if not isinstance(path, str):
      raise Exception("The path must be a string")
    if not isinstance(verbose, bool):
      raise Exception("The verbose must be a bool")

    f = open(path, 'w')
    f.write("digraph G {\n")
    # nodes
    for n in self.nodes_list:
      attr = f"[label=\"{n.label}"
      if verbose:
        attr += f"\\n id: {n.id}"
      attr += "\""
      
      if n.id in self.inputs_ids:
        attr += ",shape=\"box\""
      if n.id in self.outputs_ids:
        attr += ",shape=\"diamond\""
      
      attr += "]"
      f.write(f"n{n.id} {attr};\n")
    #edges
    for a,b in self.edges:
      f.write(f"n{a} -> n{b}\n")
    f.write("}")
    f.close()



  def save_as_pdf_file(self, path : str = "dot_files/open_digraph/graph.dot", verbose : bool = False) -> str :
      """
      Saves the graph in a pdf file
      The verbose adds the id in the file, not only the label of a node
      The add argument says if we add the graph at the end of the file
      Returns the path of the pdf_file (useful for display)
      """
      if not isinstance(path, str):
        raise Exception("The path must be a string")
      if not isinstance(verbose, bool):
        raise Exception("The verbose must be a bool")

      n_path = (''.join(str(e)+"/" for e in path.split("/")[:-1]))+"output/"+(path.split("/")[-1].split(".")[0]+".pdf") 

      self.save_as_dot_file(path, verbose)
      os.system(f"dot -Tpdf \"{path}\" -Glabel=\"{self.desc}\" -o \"{n_path}\"")
      return n_path



  def display(self, path : str = "dot_files/open_digraph/graph.dot", verbose : bool = False) -> None :
      """
      Saves and display the graph in a pdf
      The verbose adds the id in the file, not only the label of a node
      """
      if not isinstance(path, str):
        raise Exception("The path must be a string")
      if not isinstance(verbose, bool):
        raise Exception("The verbose must be a bool")

      n_path = self.save_as_pdf_file(path, verbose)
      os.system(f"xdg-open \"{n_path}\"")