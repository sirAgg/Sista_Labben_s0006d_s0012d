from Grupp2 import overlord, enums
import fog_of_war, demo, enum, math


class EntityManager():
    def __init__(self):
        self.updateState = 0
        self.trees = set()
        self.ironore = set()

        self.soldiers = {}
        self.workers = {}
        self.buildings = {}

        self.incrementUpdateState = demo.IncrementalIteration()
        self.incrementUpdateState.view_i = 0
        self.incrementUpdateState.index = 0
        self.new_trees = set()

    def updatetUnManageEntities(self):
        updateState = enums.updateOrder[self.updateState]
        if updateState == enums.UpdateState.TREES:
            def updateTrees(entity, tree):
                x = int(tree.position.x)
                y = int(tree.position.z)
                if fog_of_war.grupp2.is_discovered(x, y):
                    self.new_trees.add(entity.toInt())

            demo.ForTreeLimit(self.incrementUpdateState, updateTrees)

            if self.incrementUpdateState.view_i == 0 and self.incrementUpdateState.index == 0:
                self.trees = self.new_trees
                self.new_trees = set()
                overlord.overlord.AddScoutedTree(self.sortingTrees())

        elif updateState == enums.UpdateState.IRON:
            ownedIron = set()

            def updateIron(entity, iron):
                nonlocal ownedIron
                x = int(iron.position.x)
                y = int(iron.position.z)
                if fog_of_war.grupp2.is_discovered(x, y):
                    ownedIron.add(entity.toInt())

            demo.ForIron(updateIron)
            self.ironore = ownedIron
            overlord.overlord.AddScoutedIron(self.sortingIron())
            # send to overlord
        elif updateState == enums.UpdateState.ENEMIES:
            workers = set()
            soldiers = set()
            buildings = set()

            def updateEnemyAgents(entity, agent, team):
                nonlocal workers, soldiers
                if team.team == demo.teamEnum.GRUPP_2:
                    return
                x = int(agent.position.x)
                y = int(agent.position.z)
                if fog_of_war.grupp2.is_discovered(x, y):
                    if agent.type == demo.agentType.SOLDIER:
                        soldiers.add(entity.toInt())
                    else:
                        workers.add(entity.toInt())

            def updateEnemyBuildings(entity, building, team):
                nonlocal buildings
                if team.team == demo.teamEnum.GRUPP_2:
                    return

                x = int(building.position.x)
                y = int(building.position.z)

                if fog_of_war.grupp2.is_discovered(x, y):
                    buildings.add(entity.toInt())
                    if building.type == demo.buildingType.CASTLE:
                        overlord.overlord.AddScoutedEnemyCastle(entity)

            demo.ForAgentTeam(updateEnemyAgents)
            demo.ForBuildingTeam(updateEnemyBuildings)

            self.enemy_workers = workers
            self.enemy_soldiers = soldiers
            self.enemy_buildings = buildings
            overlord.overlord.AddScoutedWorkers(self.setTolistOfEntetys(self.enemy_workers))
            overlord.overlord.AddScoutedSoldiers(self.setTolistOfEntetys(self.enemy_soldiers))
            overlord.overlord.AddScoutedBuildings(self.setTolistOfEntetys(self.enemy_buildings))

        self.updateState = (self.updateState + 1) % len(enums.updateOrder)

    def setTolistOfEntetys(self, s: ()):
        temp = []
        for i in s:
            temp.append(demo.Entity.fromInt(i))
        return temp

    def sortingTrees(self):
        temp = []
        distans = []
        distreeTuppler =[]
        for tree in self.setTolistOfEntetys(self.trees):
            try:
                x = math.fabs(overlord.overlord.castleEntity.Building.position.x - tree.Tree.position.x)
                z = math.fabs(overlord.overlord.castleEntity.Building.position.z - tree.Tree.position.z)
            except:
                return temp
            pi = math.sqrt(x*x + z*z)
            distans.append(pi)
            distreeTuppler.append((tree, pi))

        distans.sort()

        for i in distans:
            for j in distreeTuppler:
                if i == j[1]:
                    temp.append(j[0])

        return temp

    def sortingIron(self):
        temp = []
        distans = []
        disfeTuppler =[]
        for iron in self.setTolistOfEntetys(self.ironore):
            try:
                x = math.fabs(overlord.overlord.castleEntity.Building.position.x - iron.Iron.position.x)
                z = math.fabs(overlord.overlord.castleEntity.Building.position.z - iron.Iron.position.z)
            except:
                return temp
            pi = math.sqrt(x*x + z*z)
            distans.append(pi)
            disfeTuppler.append((iron, pi))

        distans.sort()

        for i in distans:
            for j in disfeTuppler:
                if i == j[1]:
                    temp.append(j[0])

        return temp
entitymanger = EntityManager()
