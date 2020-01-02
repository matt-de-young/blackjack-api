from orator.migrations import Migration


class Init(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("users") as table:
            table.increments("id")
            table.string("username").unique()
            table.binary("password")
            table.integer("bank").default(1000)
            table.timestamps()

        with self.schema.create("games") as table:
            table.increments("id")
            # table.integer("dealer_hand_id", unsigned=True)
            table.json("deck")
            table.timestamps()

            # table.foreign("dealer_hand_id").references("id").on("hands")

        with self.schema.create("hands") as table:
            table.increments("id")
            table.integer("user_id", unsigned=True).nullable()
            table.integer("game_id", unsigned=True)
            table.boolean("is_dealer_hand").default(False)
            table.json("cards")
            table.integer("bet").nullable()
            table.timestamps()

            table.foreign("user_id").references("id").on("users").on_delete('cascade')
            table.foreign("game_id").references("id").on("games").on_delete('cascade')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("users")
        self.schema.drop("games")
        self.schema.drop("hands")
