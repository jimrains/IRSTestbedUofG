library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.ALL;

entity main is
    port (
        sw : in std_logic_vector(3 downto 0);
        led : out std_logic_vector(3 downto 0);
        ja : out std_logic_vector(7 downto 0);
        jb : out std_logic_vector(7 downto 0);
        btn : in std_logic_vector(3 downto 0);
        CLK100MHZ : in std_logic;
        ck_io26 : in std_logic; -- SCLK
        ck_io28 : in std_logic; -- DATA
        ck_io30 : in std_logic;  -- RW
        ck_io32 : out std_logic;  -- DONE
        led0_r : out std_logic := '0';
        led1_r : out std_logic := '0'        
        );
end main;

architecture Behavioral of main is

      SIGNAL S1 : std_logic := '0';
      SIGNAL S2 : std_logic := '0';
      SIGNAL R1 : std_logic := '0';
      SIGNAL R2 : std_logic := '0';
      SIGNAL memory : std_logic_vector(8 downto 0); -- 9-bit output
      SIGNAL shift : std_logic_vector(8 downto 0); -- 9-bit output
      SIGNAL seqcount : integer;
      SIGNAL regcount : integer;
      SIGNAL slotcount : integer;
      SIGNAL outcount : integer;
      SIGNAL s2count : integer := 0;
      --RAM
      SIGNAL WR : std_logic;  -- chip enable, write enable
      SIGNAL CE : std_logic;  -- chip enable, write enable
      SIGNAL A : std_logic_vector(5 downto 0); -- address
      SUBTYPE cell IS std_logic_vector(8 downto 0); -- cells are 9 bits long
      TYPE memArray IS array(0 to 63) OF cell; 
--                IC:(987654321)      Q8           Q7          Q6             Q5          Q4           Q3           Q2          Q1       -- Outputs of ICs at pin QX
      SIGNAL D : memArray  := ("000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000",  -- sequence 1  IC1: (0 0 1 0 1 0 0 0)
                               "000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000",  -- sequence 2       (0 0 0 0 1 0 0 0)
                               "000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000",  --                  (0 0 1 0 1 0 0 0)
                               "000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000",  --                  (0 0 0 0 1 0 0 0)
                               "000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000",  --                  (0 0 1 0 0 0 0 0)
                               "000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000",  --                  (0 0 0 0 0 0 0 0)
                               "000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000",  --                  (0 0 1 0 0 0 0 0)
                               "000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000", "000000000"); -- data             (0 0 0 0 0 0 0 0)
                                                                                                                                        
      SIGNAL SCLK : std_logic;  -- Pi clock line
      SIGNAL DATA : std_logic;  -- Pi data line
      SIGNAL RW : std_logic;    -- Pi r/w write high, shift out low                                                                                                                                         
      SIGNAL wraddr : integer;  -- Write address counter value
      SIGNAL countbit : integer;                                                                                                                                  
                                                                                                                                        
BEGIN
    RW <= ck_io30;
    SCLK <= ck_io26;
    DATA <= ck_io28;    
    ck_io32 <= R2;
    
    -- CLOCK HIERARCHY: SR1 > R1 > SR2 > R2 > SR3 > R3
    
    -- function to receive SPI    
    PROCESS(SCLK)
    BEGIN          
        IF rising_edge( SCLK ) THEN
            IF RW = '1' THEN
                D(wraddr) <= D(wraddr)(8 downto 0) & DATA;
                countbit <= countbit + 1;
                IF ( countbit = 8 ) THEN  -- After 9 clock and data combos, shift out data                 
                    D(wraddr) <= D(wraddr)( 8 downto 0 ) & DATA;
                    countbit <= 0;
                    wraddr <= wraddr + 1;                
                END IF;
            ELSIF RW = '0' THEN
                wraddr <= 0;
            END IF;
        END IF;                               
     END PROCESS;
     
    -- Clock generation
    SRclock1 : ENTITY work.clockDV(Behavioral)
    GENERIC MAP(
        -- clock_frequency => 2
        --clock_frequency => 12000000
        --clock_frequency =>  6000000
        --clock_frequency =>  640000
        clock_frequency => 640000
        )
    PORT MAP(
        clock_in => CLK100MHZ,
        clock_out => S1
    );
        
    shift(8 downto 0) <= D(slotcount);
        
    PROCESS( S1 )
    BEGIN
        IF (falling_edge(S1) and RW = '0') THEN            
            memory <= shift;            
        END IF;
    END PROCESS;

    PROCESS(S1)
    BEGIN
       IF RW = '1' THEN    -- Added to reset counters when async sig. RW high (write) 
            regcount <= 0;  -- P
            slotcount <= 0; -- P
            s2count <= 0; -- Reset to default value
            s2 <= '0';                        
        ELSIF (rising_edge(S1) and RW = '0') THEN
            regcount <= regcount + 1;
            slotcount <= slotcount + 1;
            s2count <= s2count + 1;
            IF regcount = 7 THEN  -- R1 not being generated      
                R1 <= '1';
                regcount <= 0;
            ELSE
                R1 <= '0';
            END IF;
            IF s2count = 8 THEN
                S2 <= '1';
                s2count <= 1;
            ELSE
                S2 <= '0';
            END IF;
--            IF slotcount = 63 THEN
--                slotcount <= 0;                
--            END IF;
        END IF;
    END PROCESS;  



    PROCESS( S2, RW )
    BEGIN
        IF RW = '1' THEN
            outcount <= 0;
        ELSIF (falling_edge(S2) and RW = '0') THEN
            outcount <= outcount + 1; -- Count for S2 to enable final register output
            IF outcount = 7 THEN
                R2 <= '1';
                outcount <= 0;                
            ELSE
                R2 <= '0';
            END IF;
        END IF;        
    END PROCESS;

-- Only valid when not mapping bits (check LED states to see if bits shifted in correctly)
    led0_r <= memory(0);
    led1_r <= memory(1);
    led(0) <= memory(2);
    led(1) <= memory(3);
    led(3) <= memory(4);
    led(2) <= memory(5);
    
    jb(7) <= memory(5);
    jb(6) <= S1;        
    jb(5) <= memory(4);               
    jb(4) <= memory(3);
    jb(3) <= memory(6);
    jb(2) <= S1;
    jb(1) <= memory(7);
    jb(0) <= R2; -- Also can act as 'done' feedback signal to Pi    
       
    ja(7) <= S1;
    ja(6) <= memory(2);        
    ja(5) <= R1;               
    ja(4) <= memory(1);
    ja(3) <= memory(8);
    ja(2) <= S2;
    ja(1) <= memory(0);
    ja(0) <= S1;               

end Behavioral;







