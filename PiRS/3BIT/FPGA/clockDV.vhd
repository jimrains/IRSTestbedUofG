
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.ALL;

entity clockDV is
  Generic(
    clock_frequency : INTEGER := 2
  );
  Port (
    clock_in : in std_logic;
    clock_out : out std_logic
     );
end clockDV;

architecture Behavioral of clockDV is

    SIGNAL clock_sig : std_logic;
    SIGNAL counter : INTEGER := 1;
    SIGNAL count_value : INTEGER := 100000000/(clock_frequency*2);
BEGIN

PROCESS ( clock_in ) IS
BEGIN
    IF rising_edge( clock_in ) THEN
        IF counter = count_value THEN
            counter <= 1;
            clock_sig <= NOT clock_sig;
        ELSE
            counter <= counter + 1;
        END IF;
    END IF;
    clock_out <= clock_sig;
                 
END PROCESS; 

END Behavioral;
