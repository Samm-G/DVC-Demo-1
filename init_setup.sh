# Conda Env Creator Script: 
# © Samm-G
# Github: https://github.com/Samm-G

# TODO: Refactor..

echo [$(date)]: "START - init-setup.bash"
echo [$(date)]: "creating environment"

if ! [ -d "conda_env" ]; then
    conda create --prefix ./conda_env python=3.7 -y
else
    echo [$(date)]: "Conda Env Already Exists"
fi

echo [$(date)]: "Activating Environment"
source activate ./conda_env

if ! [ -e "requirements.txt" ]; then
    echo [$(date)]: "requirements.txt Missing, for new conda env."
else
    echo [$(date)]: "Installing Requirements from requirements.txt"
    pip install -r requirements.txt

    echo [$(date)]: "Exporting newly created conda environment"
    conda env export > conda.yaml
fi

# TODO: For automatically adding and Committing.. 
# echo "# ${PWD}" > README.md
# echo [$(date)]: "first commit"
# git add .
# git commit -m "first commit"
echo [$(date)]: "END"


# To Revert Back everything (Or only seleted files and folders)

# rm -rf conda_env/ 
# rm -rf .gitignore 
# rm -rf conda.yaml 
# rm -rf README.md 
# rm -rf .git/