from threading import RLock

from Powers.database import MongoDB

INSERTION_LOCK = RLock()

class PINFO(MongoDB):
    """Class to store participants info"""
    db_name = "pinfo"

    def __init__(self):
        super().__init__(self.db_name)
    
    def save_pinfo(
        self,
        p_id, #participant's id
        c_id, #where user have participated
        votes=0 #total number of votes
        ):
        with INSERTION_LOCK:
            curr = self.find_one({"pa_id":p_id,"chat_id":c_id})
            if curr:
                return True
            else:
                self.insert_one(
                    {
                        "pa_id":p_id,
                        "chat_id":c_id,
                        "votes":votes
                    }
                )
                return
    
    def total_participants(self,c_id):
        with INSERTION_LOCK:
            curr = self.find_all({"chat_id":c_id})
            if curr:
                return len(curr)
            else:
                return False
    
    def update_votes(self,c_id,p_id,is_deduct=False):
        with INSERTION_LOCK:
            curr = self.find_one({"pa_id":p_id,"chat_id":c_id})
            if curr:
                vote = curr["votes"] + 1
                if is_deduct:
                    vote = curr["votes"] - 1
                self.update(
                    {"pa_id":p_id,"chat_id":c_id},
                    {"votes":vote}
                )
                return

    def get_cur_votes(self,p_id,c_id):
        with INSERTION_LOCK:
            curr = self.find_one({"pa_id":p_id,"chat_id":c_id})
            if curr:
                return curr["votes"]
            return 0

    def get_all_part(self,c_id):
        with INSERTION_LOCK:
            curr = self.find_all({"chat_id":c_id})
            if curr:
                puser = [int(i["pa_id"]) for i in curr]
                return puser


    def delete_info(self,c_id):
        with INSERTION_LOCK:
            curr = self.find_one({"chat_id":c_id})
            if curr:
                self.delete_one({"chat_id":c_id})
            return

    def get_max_votes(self,c_id):
        with INSERTION_LOCK:
            curr = self.find_all({"chat_id":c_id})
            if curr:
                max_val = max([i["votes"] for i in curr])
                users = []
                for i in curr:
                    if i["votes"] == max_val:
                        users.append(i)
                return max_val, users
                
            
