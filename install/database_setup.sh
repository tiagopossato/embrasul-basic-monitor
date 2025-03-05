# This file must be used with "source database_setup" *from bash*
# you cannot run it directly

source install_common_functions.sh

# install postgresql
printMessage "Installing postresql"
sudo apt -y install postgresql postgresql-contrib

printMessage "Creating users"
# create database user monitor with password monitor if not exists
sudo -u postgres psql -c "CREATE USER monitor WITH PASSWORD 'monitor';"

# create database user grafana with password grafana if not exists
sudo -u postgres psql -c "CREATE USER grafana WITH PASSWORD 'grafana';"

# change postgres password to postgres
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"

printMessage "Creating database"
# create database monitor if not exists
sudo -u postgres psql -c "CREATE DATABASE monitor WITH OWNER = postgres \
                            ENCODING = 'UTF8' TABLESPACE = pg_default \
                            CONNECTION LIMIT= -1;"

printMessage "Configuring database"
# set port to default 5432
sudo pg_conftool set port 5432

# https://medium.com/@mglaving/how-to-set-up-postgresql-12-to-use-a-ramdisk-for-temporary-statistics-files-on-a-raspberry-pi-4-b534a6d679ff

# set up PostgreSQL 12 to use a ramdisk for temporary statistics files

# Create directory for the ramdisk mount:
# sudo mkdir -v /mnt/ramdisk

# Give everyone full access:
# sudo chmod -v 777 /mnt/ramdisk

# if "/mnt/ramdisk" not exists in /etc/fstab, add it
# if ! grep -q "/mnt/ramdisk" /etc/fstab; then
#     # echo "/mnt/ramdisk not found in /etc/fstab"
#     # echo "adding /mnt/ramdisk to /etc/fstab"
#     sudo su -c "echo 'tmpfs /mnt/ramdisk tmpfs rw,size=100M 0 0' >> /etc/fstab"
# fi

# Mount filesystems not already mounted, i.e. the ramdisk we just added:
# sudo mount -a

# change line in postgresql.conf that start with stats_temp_directory to the following:
# sudo pg_conftool set stats_temp_directory /mnt/ramdisk/postgresql/13-main.pg_stat_tmp
# pg_conftool get stats_temp_directory
# set timezone to UTC
sudo pg_conftool set timezone 'UTC'

# variable with sql instructions to create table
create_table='CREATE TABLE IF NOT EXISTS sensors_data (
                id SERIAL PRIMARY KEY,
                node SMALLINT NOT NULL,
                object SMALLINT NOT NULL,
                instance SMALLINT NOT NULL,
                resource SMALLINT NOT NULL,
                value NUMERIC,
                sync boolean DEFAULT false,
                timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
                CONSTRAINT sensors_data_unique_idx UNIQUE (node, object, instance, resource, timestamp)
            );


            ALTER TABLE IF EXISTS public.sensors_data OWNER to postgres;
            GRANT ALL ON TABLE public.sensors_data TO postgres;            
            GRANT USAGE, SELECT ON SEQUENCE sensors_data_id_seq TO monitor;
            GRANT SELECT, INSERT, UPDATE ON TABLE public.sensors_data TO monitor;
            GRANT SELECT ON TABLE public.sensors_data TO grafana;
            '

# execute sql instructions
# printMessage "Creating table sensors_data"
# sudo -u postgres psql -c "$create_table" -d monitor

# restart postgresql service
printMessage "Restarting postgresql service"
sudo systemctl restart postgresql.service