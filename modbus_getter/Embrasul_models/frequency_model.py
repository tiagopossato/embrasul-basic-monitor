from SunSpec import Model, PointGroup, Point, point_type

frequency_model = Model(id=2, start_address=66, update_interval=30,
    group = PointGroup(id="2", name="Frequência", label="Frequência da rede", 
    points = [
        Point(id='FreqA', size=2, label='Frequência A', description='Frequência na fase A',  pt_type=point_type.float32, units="Hz"),
    ]))