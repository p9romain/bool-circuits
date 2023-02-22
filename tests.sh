rm dot_files/*.dot dot_files/output/*.pdf
rm dot_files/random/*.dot dot_files/random/output/*.pdf

clear
for FILE in tests/* ; 
do python3 $FILE ;
echo "



" ; 
done