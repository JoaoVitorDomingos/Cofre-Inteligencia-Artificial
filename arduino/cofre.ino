#include <LiquidCrystal.h>
#include <Servo.h>

// LCD
LiquidCrystal lcd(5, 6, 7, 8, 9, 10);

// Aqui estamos criando o servo
Servo servoMotor;

// Pinos utilizados
//Os pinos do LCD é o D5 até o D10
int pinoPotencia = A0;
int pinoBotao = 2;
int pinoLedVermelho = 11;
int pinoLedVerde = 12;
int buzzer = 4;

// SENHA PADRÃO
int senha[3] = {200, 400, 800};
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

// IA
bool modoIA = true;

bool acessoLiberado = false;

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
    nivelBloqueio++;

    // 15s, 30s, 45s...
    duracaoBloqueio = nivelBloqueio * 15000;

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

  if (modoIA)
  {
    lcd.print("Face OK");
  }
  else
  {
    lcd.print("Acesso");
  }

  lcd.setCursor(0, 1);

  if (modoIA)
  {
    lcd.print("Liberado IA");
  }
  else
  {
    lcd.print("Liberado");
  }

  servoMotor.write(0);

  digitalWrite(pinoLedVerde, HIGH);

  tone(buzzer, 1200, 500);

  delay(3000);

  digitalWrite(pinoLedVerde, LOW);

  servoMotor.write(90);

  etapaAtual = 0;
  tentativas = 0;

  delay(500);

  if (!modoIA)
  {
    while (digitalRead(pinoBotao) == LOW);
  }

  lcd.clear();

  // Se estiver em modo IA, volta para a tela de espera
  if (modoIA)
  {
    lcd.setCursor(0, 0);
    lcd.print("Modo IA");

    lcd.setCursor(0, 1);
    lcd.print("Aguardando...");
  }
}

// --------------------------------------------------

void verificarSerial()
{
  while (Serial.available())
  {
    char comando = Serial.read();

    if (comando == '\n' || comando == '\r')
      continue;

    if (comando == '1')
    {
      if (!acessoLiberado)
      {
        acessoLiberado = true;
        abrirCofre();
      }
    }

    else if (comando == '0')
    {
      acessoLiberado = false;
    }
  }
}

// --------------------------------------------------

void setup()
{
  Serial.begin(9600);
  pinMode(pinoBotao, INPUT_PULLUP);

  pinMode(pinoLedVerde, OUTPUT);
  pinMode(pinoLedVermelho, OUTPUT);

  servoMotor.attach(3);
  servoMotor.write(90);

  lcd.begin(16, 2);

  lcd.setCursor(0, 0);
  lcd.print("Cofre Digital");

  lcd.setCursor(0, 1);
  lcd.print("Inicializando");

  delay(2000);

  lcd.clear();

  delay(500);

  if (modoIA)
  {
      lcd.clear();

      lcd.setCursor(0,0);
      lcd.print("Modo IA");

      lcd.setCursor(0,1);
      lcd.print("Aguardando...");
  }
}

// --------------------------------------------------

void loop()
{
  if (modoIA)
  {
    verificarSerial();
    return;
  }

  int valor = analogRead(pinoPotencia);

  // BLOQUEIO
  if (bloqueado)
  {
    tone(buzzer, 800, 500);
	delay(200);

	tone(buzzer, 1000, 500);
	delay(200);
    
    lcd.setCursor(0, 0);
    lcd.print("ALARME ATIVO   ");

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
    // Debounce
    delay(50);

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