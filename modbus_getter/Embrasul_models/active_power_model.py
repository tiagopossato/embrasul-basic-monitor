from SunSpec import Model, PointGroup, Point, point_type

active_power_model = Model(id=4, start_address=80, update_interval=10,
    group = PointGroup(id="1", name="Potência ativa", label="Potência ativa", 
    points = [
        Point(id='PotAtivA', size=2, label='Potência ativa A', description='Potência ativa na fase A',  pt_type=point_type.float32, units="W"),
        Point(id='PotAtivB', size=2, label='Potência ativa B', description='Potência ativa na fase B',  pt_type=point_type.float32, units="W"),
        Point(id='PotAtivC', size=2, label='Potência ativa C', description='Potência ativa na fase C',  pt_type=point_type.float32, units="W"),
        Point(id='PotAtivT', size=2, label='Potência ativa Total', description='Potência ativa Total',  pt_type=point_type.float32, units="W"),
    ]))
