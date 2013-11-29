class CreateMeats < ActiveRecord::Migration
  def up
    create_table :meats do |t|
      t.string   :key
      t.string   :gif
      t.string   :message
      t.integer  :created 
      t.string   :fingerprint

      t.timestamps
    end
  end

  def down
    drop_table :meats
  end
end