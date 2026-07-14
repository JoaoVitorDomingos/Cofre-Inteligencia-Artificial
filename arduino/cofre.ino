#include <LiquidCrystal.h>
#include <Servo.h>

// LCD Configurado nos pinos digitais de 2 a 5, 11 e 12
// LiquidCrystal lcd(RS, RW, E, D4, D5, D6, D7)
LiquidCrystal lcd(12, 11, 10, 5, 4, 3, 2);

// Instanciando o servo
Servo servoMotor;

// Pinos utilizados REORGANIZADOS
const int pinoPotencia = A0;      // Potenciômetro do segredo
const int pinoBotao = A1;         // Botão de confirmação
const int pinoLedVerde = A2;      // LED de acerto
const int pinoLedVermelho = A3;   // LED de erro/bloqueio
const int buzzer = 7;             // Buzzer livre no pino 7
const int pinoServo = 6;          // Servo livre e no PWM do pino 6
const int pinoLedLCD = 13;

// SENHA PADRÃO
int senha[3] = {200, 400, 600};
int toleranciaSenha = 50;

// CONTROLE DE ETAPAS
int etapaAtual = 0;

// TENTATIVAS
int tentativas = 0;

// BLOQUEIO
bool bloqueado = false;
unsigned long inicioBloqueio = 0;
unsigned long duracaoBloqueio = 0;
int nivelBloqueio = 0;

// TIMEOUT
unsigned long ultimoAcerto = 0;
unsigned long tempoTimeout = 10000;

// Controle da IA
bool iaLiberou = false;
bool isIAAtivada = false;
bool mensagemIAExibida = false;

// --------------------------------------------------

bool dentroFaixa(int valor, int alvo)
{
  return valor >= (alvo - toleranciaSenha) &&
         valor <= (alvo + toleranciaSenha);
}

// --------------------------------------------------

void piscarVerde()
{
  digitalWrite(pinoLedVerde, HIGH);
  delay(300);
  digitalWrite(pinoLedVerde, LOW);
}

// --------------------------------------------------

void erro()
{
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Senha Errada");

  lcd.setCursor(0, 1);
  lcd.print("Tentativa ");
  lcd.print(tentativas + 1);

  digitalWrite(pinoLedVermelho, HIGH);
  tone(buzzer, 400, 500);

  delay(1500);

  digitalWrite(pinoLedVermelho, LOW);

  etapaAtual = 0;
  tentativas++;

  if (tentativas >= 3)
  {
    duracaoBloqueio = 5000;

    bloqueado = true;
    inicioBloqueio = millis();
  }

  delay(2000);
  lcd.clear();
}

// --------------------------------------------------

void abrirCofre()
{
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Acesso");

  lcd.setCursor(0, 1);
  lcd.print("Liberado");

  servoMotor.write(0); // Abre a trava

  digitalWrite(pinoLedVerde, HIGH);
  tone(buzzer, 1200, 500);

  delay(3000);

  digitalWrite(pinoLedVerde, LOW);
  
  servoMotor.write(90); // Tranca novamente após o tempo de abertura

  etapaAtual = 0;
  tentativas = 0;

  delay(500);

  while (digitalRead(pinoBotao) == LOW);

  lcd.clear();
}

// --------------------------------------------------

void lerIA()
{
    while (Serial.available())
    {
        isIAAtivada = true;

        char comando = Serial.read();

        if (comando == '1')
        {
            iaLiberou = true;
        }

        if (comando == '0')
        {
            iaLiberou = false;
        }
    }
}

// --------------------------------------------------

void cofre(int valor)
{
  // TELA PRINCIPAL
  lcd.setCursor(0, 0);
  lcd.print("Senha ");
  lcd.print(etapaAtual + 1);
  lcd.print("/3      ");

  lcd.setCursor(0, 1);
  lcd.print("Valor:");
  lcd.print(valor);
  lcd.print("     ");

  // BOTÃO PRESSIONADO
  if (digitalRead(pinoBotao) == LOW)
  {
    delay(50); // Debounce

    if (digitalRead(pinoBotao) == LOW)
    {
      if (dentroFaixa(valor, senha[etapaAtual]))
      {
        lcd.clear();

        lcd.setCursor(0, 0);
        lcd.print("Etapa Correta");

        lcd.setCursor(0, 1);
        lcd.print(etapaAtual + 1);
        lcd.print("/3");

        tone(buzzer, 1500, 500);
        piscarVerde();

        etapaAtual++;
        ultimoAcerto = millis();

        delay(1500);
        lcd.clear();

        if (etapaAtual >= 3)
        {
            abrirCofre();

            while (digitalRead(pinoBotao) == LOW);
        }

        return;
      }
      else
      {
        erro();
        while (digitalRead(pinoBotao) == LOW);
        return;
      }
    }
  }
}

// --------------------------------------------------

void setup()
{
  Serial.begin(9600);
  
  // Configuração dos pinos
  pinMode(pinoBotao, INPUT_PULLUP);
  pinMode(pinoLedVerde, OUTPUT);
  pinMode(pinoLedVermelho, OUTPUT);
  pinMode(buzzer, OUTPUT);
  
  pinMode(pinoLedLCD, OUTPUT);
  digitalWrite(pinoLedLCD, HIGH);
  
  // Inicialização do Servo no pino correto (6)
  servoMotor.attach(pinoServo);
  servoMotor.write(90); // Posição trancado padrão

  // Inicialização do LCD
  lcd.begin(16, 2);

  lcd.setCursor(0, 0);
  lcd.print("Cofre Digital");

  lcd.setCursor(0, 1);
  lcd.print("Inicializando");

  delay(1000);
  lcd.clear();

  isIAAtivada = false;
}

// --------------------------------------------------

void loop()
{
  lerIA();

  int valor = analogRead(pinoPotencia);
  lcd.display();
  
  // BLOQUEIO
  if (bloqueado)
  {
    tone(buzzer, 800, 500);
    delay(200);

    tone(buzzer, 1000, 500);
    delay(200);
    
    lcd.setCursor(0, 0);
    lcd.print("ALARME ATIVO    ");

    lcd.setCursor(0, 1);
    lcd.print("Cofre Travado  ");

    digitalWrite(pinoLedVermelho, HIGH);
    delay(300);

    digitalWrite(pinoLedVermelho, LOW);
    delay(300);

    if (millis() - inicioBloqueio >= duracaoBloqueio)
    {
      noTone(buzzer);
      bloqueado = false;
      tentativas = 0;
      lcd.clear();
    }

    return;
  }

  // TIMEOUT
  if (etapaAtual > 0)
  {
    if (millis() - ultimoAcerto > tempoTimeout)
    {
      etapaAtual = 0;

      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Tempo Excedido");

      digitalWrite(pinoLedVermelho, HIGH);
      delay(1000);
      digitalWrite(pinoLedVermelho, LOW);
      delay(2000);

      lcd.clear();
      return;
    }
  }

  // IA conectada e rosto bloqueado
  if (isIAAtivada && !iaLiberou)
  {
      etapaAtual = 0;

      if (!mensagemIAExibida)
      {
          lcd.clear();

          lcd.setCursor(0,0);
          lcd.print("Rosto Obstruido");

          lcd.setCursor(0,1);
          lcd.print("Cofre Bloqueado");

          mensagemIAExibida = true;
      }

      // Impede qualquer operação do cofre
      return;
  }

  // Se chegou aqui, pode usar normalmente
  mensagemIAExibida = false;

  cofre(valor);
}