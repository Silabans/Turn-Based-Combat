from abc import ABC, abstractmethod
import random as r

class Combatant(ABC):
    def __init__(self, name: str):
        """Contains default values for the character."""
        self.classtype = "Combatant"
        self.name = name
        self.start_health = 100
        self.health = 100
        self.max_damage = 30
        self.dmg_mult = 1
        #This is the multiplier for the damage received
        self.parry_success = [10, 50]
        self.parrying = False
        self.bleeding = False
        self.bleed_duration = 0
        self.stunned = False
        self.crit_rate = 10
        self.sig_cd = 0
        #Cooldown for signature move

    def __str__(self):
        """Returns the character's name and class type."""
        return f"{self.name} ({self.classtype})"
        

    def preturn_check(self) -> bool:
        """Returns True if not stunned; False otherwise.
        
        Drains health if bleed is ongoing.
        """
        if self.sig_cd > 0:
            self.sig_cd -= 1

        if self.bleeding:
            damage = round(0.1 * self.start_health)
            self.health -= damage
            self.bleed_duration -= 1
            print(f"{self.name} is bleeding and loses {damage} HP...")
        
        if self.bleed_duration <= 0:
            self.bleeding = False
            print(f"Bleeding has stopped for {self}.")
        
        if self.stunned:
            print(f"{self.name} is still dazed! Turn is skipped")
            self.stunned = False
            return False
        return True

    def attack(self, opponent, modifier=1.0) -> str:
        """Serves as the main form of retaliation against an opponent."""
        is_crit = r.randint(1, 100) <= self.crit_rate
    
        damage = r.randint(int(self.max_damage/2), self.max_damage) * modifier
        actual_dmg = round(opponent.dmg_mult * damage * 1.5 if is_crit else opponent.dmg_mult * damage)
        opponent.health -= actual_dmg
        output_msg = f"{self.name} attacks for {actual_dmg} damage!"

        if opponent.parrying:
            reflected_dmg = ((1.0 - opponent.dmg_mult)/2)*damage
            self.health -= reflected_dmg
            if opponent.dmg_mult == 0.5:
                output_msg += f"\n{self.name} has been PARTIALLY parried! {reflected_dmg} damage is reflected."
            elif opponent.dmg_mult == 0:
                output_msg += f"\n{self.name} has been COMPLETELY parried! {reflected_dmg} damage is reflected."
            else:
                output_msg += f"\n{self.name} broke the parry! Noob parry by {opponent.name}."
        

        opponent.dmg_mult = 1
        opponent.parrying = False
        #Reverts the damage multiplier to the base level & resets parrying to False
        return output_msg



    def parry(self, opponent) -> str:
        """Based on the level of success, partially or completely blocks and reflects
        your opponent's attack.
        """
        self.parrying = True
        floor = self.parry_success[0]
        ceiling = self.parry_success[1]
        success_rate = r.randint(floor, ceiling)
        if success_rate > 65:
            #block all damage and return half the damage received
            self.dmg_mult = 0
        elif 30 <= success_rate <= 65:
            #block half the damage received and return a quarter
            self.dmg_mult = 0.5
        return f"{self.name} braces for an impact..."
    
    @abstractmethod
    def signature(self, opponent) -> str:
        """This is a unique attack/move that every class type has.
        Typically inflicts a detrimental status effect on the opponent OR a buff on self.
        """
        pass


class Tank(Combatant):
    def __init__(self, name):
        super().__init__(name)
        self.classtype = "Tank"
        self.start_health = r.randint(150, 180)
        self.health = self.start_health
        self.max_damage = 25
        self.crit_rate = 5
        self.parry_success = [20 , 100]

    def signature(self, opponent):
        if self.sig_cd == 0:
            self.sig_cd = 3
            self.attack(opponent, 0.5)
            #modifier becomes 0.5, meaning stunning attacks are half the dmg of standards attacks
            opponent.stunned = True if r.randint(1,10) > 3 else False
            #60 percent chance of stunning the enemy
            if opponent.stunned == True:
                opponent.parrying = False
                opponent.dmg_mult = 1

                return f"{opponent.name} is stunned for 1 turn!"
            else:
                return "Stun failed!"
            
        else:
            return f"Signature is still in cooldown! {self.sig_cd} turn(s) left"


class Assassin(Combatant):
    def __init__(self, name):
        super().__init__(name)
        self.classtype = "Assassin"
        self.start_health = r.randint(80, 110)
        self.health = self.start_health
        self.max_damage = 45
        self.crit_rate = 15
        self.parry_success = [10, 70]

    def signature(self, opponent) -> str:
        if self.sig_cd == 0:
            self.sig_cd = 3
            if opponent.parrying == False:
                self.attack(opponent, 0.7)
                opponent.bleeding = True if r.randint(1, 10) > 1 else False
                opponent.bleed_duration = 3
                if opponent.bleeding:
                    return f"Successful slash! {opponent.name} starts to lose blood..."
                else:
                    return "Slashing failed! No bleeding inflicted."
            else:
                return self.attack(opponent, 0.7)
        else:
            return f"Signature is still in cooldown! {self.sig_cd} turn(s) left."
        

character1 = Assassin("James")
character2 = Tank("Diddler")



def start_battle(player1: Combatant, player2: Combatant) -> str:
    turn, waiter = (player1, player2) if r.random() > 0.5 else (player2, player1)

    print(f"The battle begins! {turn.name} starts first...")

    while turn.health > 0 and waiter.health > 0:
        if not turn.preturn_check():
            turn, waiter = waiter, turn
            continue

        move = input(f"{turn.name}'s turn ({turn.classtype})- {turn.health} HP - [ 1 to attack, 2 to parry, 3 for your signature ]: ")
        if move == "1":
            print(turn.attack(waiter))
        elif move == "2":
            print(turn.parry(waiter))
        elif move == "3":
            print(turn.signature(waiter))
        else:
            print("Invalid input! Please key in 1 (attack), 2 (parry), or 3 (parry)")

        turn, waiter = waiter, turn
        
  
    if turn.health <= 0:
        return f"{waiter.name} won! Hooray!"
    
    return "wait what how are you seeing this??"

battle = start_battle(character1, character2)
    
print(battle)
