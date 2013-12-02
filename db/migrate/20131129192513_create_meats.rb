class CreateMeats < ActiveRecord::Migration
  def up
    create_table :meats do |t|
      t.string   :key
      t.text   :gif
      t.string   :message
      t.string   :hashtag
      t.column   :created , :bigint
      t.string   :fingerprint

      t.timestamps
    end
  end

  def down
    drop_table :meats
  end
end
