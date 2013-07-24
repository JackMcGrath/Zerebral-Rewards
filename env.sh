#!/bin/bash
dependencies=("django" "south" "requests")

function checkenv {
	echo "${dependencies[@]}" > one.txt
	echo "`cat .python-env/dependencies.txt`" > two.txt

	comm -23 << one.txt <two.txt
	rm one.txt two.txt
}

function rmenv {

	if [ -d ".python-env" ]; then
		rm -fr .python-env
	fi

}

function buildenv {
	echo "Building new environment"
	virtualenv --no-site-packages .python-env 
	source .python-env/bin/activate

	for dep in "${dependencies[@]}"
	do 
		echo "Installing ${dep}"
		pip install $dep
		echo "$dep" >> .python-env/dependencies.txt
	done

}

function main {
	#if env doesnt exist, build it
	if [ ! -d ".python-env" ]
	then
		echo "Python Virtualenv does not exist"
		buildenv
	fi

	#if it does exist check to see if its up to date


	#finally, lets just hop into that env
	source .python-env/bin/activate
}

#checkenv
#rmenv
main
