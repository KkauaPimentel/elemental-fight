```mermaid
classDiagram
direction TB
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

    Personagem <|-- Water
    Personagem <|-- Fire
    Personagem <|-- Air
    Personagem <|-- Earth
    Personagem <|-- Wood
