```Mermaid
classDiagram
direction TB
    class Personagem{
        +base
    }
    
    class Water{
        +Fraqueza(earth)
    }
    class Fire{
        +Fraqueza(water)
    }
    class Air{
        +Fraqueza(earth)
    }
    class Earth{
        +Fraqueza(water)
    }
    class Wood{
        +Fraqueza(fire)
    }

    Water --|> Personagem
    Fire --|> Personagem
    Air --|> Personagem
    Earth --|> Personagem
    Wood --|> Personagem
