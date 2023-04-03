from threading import RLock

from Powers.database import MongoDB

INSERTION_LOCK = RLock()

class VINFO(MongoDB):
    """Class to store voters info"""
    db_name = "vinfo"

    def __init__(self):
        super().__init__(self.db_name)

    def save_voter(
        self,
        vo_id, # Voter's id
        p_id, # Participant's id
        c_id # Chat id
    ):
        with INSERTION_LOCK:
            curr = self.find_one({"voter_id":vo_id,"pa_id":p_id,"chat_id":c_id})
            if curr:
                return True
            else:
                self.insert_one(
                    {
                        "voter_id":vo_id,
                        "pa_id":p_id,
                        "chat_id":c_id
                    }
                )
                return False

    
    def count_voters(self,c_id):
        with INSERTION_LOCK:
            curr = self.find_all({"chat_id":c_id})
            if curr:
                return len(curr)
            else:
                return 0
    
    def get_voter(self,c_id,v_id):
        with INSERTION_LOCK:
            curr = self.find_one({"voter_id":v_id,"chat_id":c_id})
            if curr:
                return curr
            else:
                return False

    def delete_voters(self,c_id):
        with INSERTION_LOCK:
            curr = self.find_all({"chat_id":c_id})
            if curr:
                self.delete_one({"chat_id":c_id})
            return
