from bpl_lib.helpers.Database import Database

class DDL:
    @staticmethod
    def ddl():
        DDL.create_tables()
        DDL.insert_into_networks()

    @staticmethod
    def create_tables():
        database = Database()
        database.insert(
            "CREATE TABLE IF NOT EXISTS Networks ("
          + "  Identifier TEXT,"
          + "  BeginEpoch TEXT,"
          + "  Version TEXT,"
          + "  PRIMARY KEY (Identifier),"
          + "  CONSTRAINT identifier_unique UNIQUE (Identifier)"
          + ");"
        )
        database.close()

    @staticmethod
    def insert_into_networks():
        networks = {
            "mainnet": {
              "begin_epoch": "2017-03-21 13:00:00",
              "version": "0x17"
            },
            "testnet": {
              "begin_epoch": "2017-03-21 13:00:00",
              "version": "0x17"
            }
        }

        database = Database()
        for config in networks.keys():
            database.insert(
                "INSERT OR IGNORE INTO Networks(Identifier, BeginEpoch, Version) "
              + "VALUES (?, ?, ?)",
                (config, networks[config]["begin_epoch"], networks[config]["version"])
            )
        database.close()
