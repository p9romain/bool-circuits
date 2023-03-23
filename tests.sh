rm dot_files/*.dot dot_files/output/*.pdf
rm dot_files/bool_circ/*.dot dot_files/bool_circ/output/*.pdf
rm dot_files/open_digraph/*.dot dot_files/open_digraph/output/*.pdf
rm dot_files/random_graph/*.dot dot_files/random_graph/output/*.pdf

clear
for FILE in tests/* ; 
do python3 $FILE ;
echo "



" ; 
done