nebula_begin_app(nebula-demo windowed)

fipsutil_copy(python_scripts.yml)
fipsutil_copy(maps.yml)

fips_dir(.)
    add_blueprint(
        data/tables/demo_blueprints.json
    )

    add_template_dir(
        data/tables/templates
    )
    
    fips_files(
        main.cc
        demogamefeatureunit.h
        demogamefeatureunit.cc
        gamestatemanager.h
        gamestatemanager.cc
        pythonbindings.h
        pythonbindings.cc
        navmesh.h
        navmesh.cc
    )

    fips_dir(managers)
        fips_files(
            playermanager.h
            playermanager.cc
            inputmanager.h
            inputmanager.cc
            movementmanager.h
            movementmanager.cc
            messagesystem.h
            messagesystem.cc
            agentmanager.h
            agentmanager.cc
        )

    fips_dir(properties)
        nebula_add_nidl(
            input.nidl
            movement.nidl
	    agent.nidl
	    health.nidl
	    team.nidl
	    building.nidl
	    iron.nidl
	    tree.nidl
        )

fips_deps(foundation application render resource dynui scripting editor)
nebula_end_app()
target_include_directories(nebula-demo PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
