from SunSpec import Model, PointGroup, Point, point_type

pf_model = Model(id=5, start_address=104, update_interval=30,
    group = PointGroup(id="5", name="Fator de potência", label="Fator de potência da rede", 
    points = [
        Point(id='FatPotA', size=2, label='Fator de Potência A', description='Fator de Potência Fase A',  pt_type=point_type.float32, units=""),
        # Point(id='FatPotB', size=2, label='Fator de Potência B', description='Fator de Potência Fase B',  pt_type=point_type.float32, units=""),
        # Point(id='FatPotC', size=2, label='Fator de Potência C', description='Fator de Potência Fase C',  pt_type=point_type.float32, units=""),
        # Point(id='FatPotT', size=2, label='Fator de Potência T', description='Fator de Potência Fase T',  pt_type=point_type.float32, units=""),
    ]))