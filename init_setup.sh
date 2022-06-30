# TODO: Refactor..
# TODO: Break down into steps.. only perform steps if the output files/folders are not present..

echo [$(date)]: "START - init-setup.bash"
echo [$(date)]: "creating environment"
conda create --prefix ./conda_env python=3.8 -y
echo [$(date)]: "activate environment"
source activate ./conda_env
echo [$(date)]: "install requirements"
pip install -r requirements.txt
echo [$(date)]: "export conda environment"
conda env export > conda.yaml
# echo "# ${PWD}" > README.md
# echo [$(date)]: "first commit"
# git add .
# git commit -m "first commit"
echo [$(date)]: "END"


# to remove everything -
# rm -rf conda_env/ # .gitignore conda.yaml README.md .git/