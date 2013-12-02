class AddIndexToKeyAndFingerprint < ActiveRecord::Migration
  def up
    add_index :meats, :key
    add_index :meats, :fingerprint
    add_index :meats, :hashtag
  end

  def down
    remove_index :meats, :key
    remove_index :meats, :fingerprint
    remove_index :meats, :hashtag
  end
end
