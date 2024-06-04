from SunSpec import Model, PointGroup, Point, point_type

voltage_model = Model(id=1, start_address=68, update_interval=2,
    group = PointGroup(id="1", name="Tensão", label="Valores de tensão", 
    points = [
        Point(id='UrmsA', size=2, label='Tensão A', description='Tensão RMS na fase A',  pt_type=point_type.float32, units="V"),
        Point(id='UrmsB', size=2, label='Tensão B', description='Tensão RMS na fase B',  pt_type=point_type.float32, units="V"),
        Point(id='UrmsC', size=2, label='Tensão C', description='Tensão RMS na fase C',  pt_type=point_type.float32, units="V"),
    ]))