from config.arguments import args      
import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_dir)
import torch


class BaseModel:
    def __init__(self, 
                 env,
                 thousands=1e-5,
                 gamma=0.9,
                 model_path = None,
                 env_size=args.env_size, 
                 start_state=args.start_state, 
                 target_state=args.target_state, 
                 forbidden_states=args.forbidden_states):
        self.env = env
        self.thousands = thousands
        self.gamma = gamma
        
        self.model_path = model_path
        self.env_size = env_size
        self.num_states = env_size[0] * env_size[1]
        self.start_state = start_state
        self.target_state = target_state
        self.forbidden_states = forbidden_states

        self.agent_state = start_state
        self.action_space = args.action_space          
        self.reward_target = args.reward_target
        self.reward_forbidden = args.reward_forbidden
        self.reward_step = args.reward_step
        
    # load the policy, action values and state values from a file
    def load(self, path):
        self.model_path = path
        assert os.path.exists(self.model_path), f"Model file '{self.model_path}' does not exist."
        
        data = torch.load(self.model_path)
        assert 'policy' in data and 'v' in data and 'q' in data, "Loaded data missing 'policy' or 'q' keys."
        
        self.policy = data['policy'].numpy()
        self.v = data['v'].numpy()
        self.q = data['q'].numpy()
        print(f"Model loaded from {self.model_path}")
        
    # save the policy, action values and state values to a file    
    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        policy_tensor = torch.tensor(self.policy, dtype=torch.float32)
        v_tensor = torch.tensor(self.v, dtype=torch.float32)
        q_tensor = torch.tensor(self.q, dtype=torch.float32)
        torch.save({'policy': policy_tensor, 'v': v_tensor, 'q':q_tensor}, path)
        print(f"Model saved to {path}")
