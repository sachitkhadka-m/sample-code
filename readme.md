#Clone the project to make sure all the submodule is downloaded along with main project

git clone --recursive <project url>

#Add submodule to the main project

git submodule add <submodule-repo-url>


#Unfortunately someone clones the main project and finds submodule empty below command will ensure they have all submodule content.

git submodule update --init --recursive

#Runs the pull for the main repo and updates the submodule as well

git pull --recurse-submodules

#Before pushing the main repository, Git checks if the submodule commits referenced by the main repo exist on the remote.

git push --recurse-submodules=check


#Git will automatically push required submodule commits first, then push the main repo.
So instead of failing like check, it pushes the missing submodule commits automatically.

git push --recurse-submodules=on-demand


