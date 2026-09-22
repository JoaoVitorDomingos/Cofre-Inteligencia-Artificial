#include <LiquidCrystal.h>
#include <Servo.h>

// ==================================================
// LCD
// LiquidCrystal lcd(RS, RW, E, D4, D5, D6, D7)
// ==================================================
LiquidCrystal lcd(12, 11, 10, 5, 4, 3, 2);

// ==================================================
// SERVO
// ==================================================
Servo servoMotor;

// ==================================================
// PINOS
// ==================================================
const int pinoPotencia = A0;      // Potenciômetro do segredo
const int pinoBotao = A1;         // Botão de confirmação
const int pinoLedVerde = A2;      // LED de acerto
const int pinoLedVermelho = A3;  // LED de erro/bloqueio
const int buzzer = 7;             // Buzzer
const int pinoServo = 6;          // Servo
const int pinoLedLCD = 13;        // Luz do LCD

// ==================================================
// SENHA PADRÃO
// ==================================================
int senha[3] = {200, 400, 600};
int toleranciaSenha = 50;

// ==================================================
// CONTROLE DE ETAPAS
// ==================================================
int etapaAtual = 0;

// ==================================================
// TENTATIVAS
// ==================================================
int tentativas = 0;

// ==================================================
// BLOQUEIO
// ==================================================
bool bloqueado = false;
unsigned long inicioBloqueio = 0;
unsigned long duracaoBloqueio = 0;
int nivelBloqueio = 0;

// ==================================================
// TIMEOUT
// ==================================================
unsigned long ultimoAcerto = 0;
unsigned long tempoTimeout = 10000;

// ==================================================
// CONTROLE DA IA
// ==================================================
bool iaLiberou = false;
bool isIAAtivada = false;
bool mensagemIAExibida = false;

// ==================================================
// VERIFICA SE O VALOR ESTÁ DENTRO DA TOLERÂNCIA
// ==================================================
bool dentroFaixa(int valor, int alvo)
{
  return valor >= (alvo - toleranciaSenha) &&
         valor <= (alvo + toleranciaSenha);
}

// ==================================================
// PISCA LED VERDE
// ==================================================
void piscarVerde()
{
  digitalWrite(pinoLedVerde, HIGH);
  delay(300);
  digitalWrite(pinoLedVerde, LOW);
}

// ==================================================
// ERRO DE SENHA
// ==================================================
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

  // Após 3 tentativas, bloqueia
  if (tentativas >= 3)
  {
    duracaoBloqueio = 5000;
    bloqueado = true;
    inicioBloqueio = millis();
  }

  delay(2000);

  lcd.clear();
}

// ==================================================
// ABRIR COFRE
// AGORA O COFRE FICA ABERTO ATÉ O BOTÃO SER PRESSIONADO
// ==================================================
void abrirCofre()
{
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Acesso");

  lcd.setCursor(0, 1);
  lcd.print("Liberado");

  // Abre a trava
  servoMotor.write(0);

  digitalWrite(pinoLedVerde, HIGH);

  tone(buzzer, 1200, 500);

  delay(1000);

  // ==================================================
  // COFRE PERMANECE ABERTO
  // ==================================================
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Cofre Aberto");

  lcd.setCursor(0, 1);
  lcd.print("Aperte o botao");

  // ==================================================
  // AGUARDA O BOTÃO SER PRESSIONADO
  // ==================================================
  while (digitalRead(pinoBotao) == HIGH)
  {
    // Fica aguardando
  }

  // Debounce
  delay(50);

  // Confirma que o botão continua pressionado
  if (digitalRead(pinoBotao) == LOW)
  {
    // ==================================================
    // FECHA O COFRE
    // ==================================================
    servoMotor.write(90);

    digitalWrite(pinoLedVerde, LOW);

    lcd.clear();

    lcd.setCursor(0, 0);
    lcd.print("Cofre Fechado");

    lcd.setCursor(0, 1);
    lcd.print("Ate logo!");

    tone(buzzer, 800, 300);

    delay(1000);

    // ==================================================
    // AGUARDA O BOTÃO SER SOLTO
    // ==================================================
    while (digitalRead(pinoBotao) == LOW)
    {
      // Aguarda soltar o botão
    }

    // ==================================================
    // RESETA O SISTEMA
    // ==================================================
    etapaAtual = 0;
    tentativas = 0;

    lcd.clear();
  }
}

// ==================================================
// LEITURA DA IA
// ==================================================
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

// ==================================================
// CONTROLE DO COFRE
// ==================================================
void cofre(int valor)
{
  // ==================================================
  // TELA PRINCIPAL
  // ==================================================
  lcd.setCursor(0, 0);

  lcd.print("Senha ");
  lcd.print(etapaAtual + 1);
  lcd.print("/3      ");

  lcd.setCursor(0, 1);

  lcd.print("Valor:");
  lcd.print(valor);
  lcd.print("     ");

  // ==================================================
  // BOTÃO PRESSIONADO
  // ==================================================
  if (digitalRead(pinoBotao) == LOW)
  {
    delay(50); // Debounce

    if (digitalRead(pinoBotao) == LOW)
    {
      // ==================================================
      // SENHA CORRETA
      // ==================================================
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

        // ==================================================
        // TODAS AS ETAPAS FORAM CONCLUÍDAS
        // ==================================================
        if (etapaAtual >= 3)
        {
          abrirCofre();

          // Garante que o botão seja liberado
          while (digitalRead(pinoBotao) == LOW)
          {
          }
        }

        return;
      }

      // ==================================================
      // SENHA ERRADA
      // ==================================================
      else
      {
        erro();

        // Aguarda soltar o botão
        while (digitalRead(pinoBotao) == LOW)
        {
        }

        return;
      }
    }
  }
}

// ==================================================
// SETUP
// ==================================================
void setup()
{
  Serial.begin(9600);

  // ==================================================
  // CONFIGURAÇÃO DOS PINOS
  // ==================================================
  pinMode(pinoBotao, INPUT_PULLUP);

  pinMode(pinoLedVerde, OUTPUT);
  pinMode(pinoLedVermelho, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(pinoLedLCD, OUTPUT);

  digitalWrite(pinoLedLCD, HIGH);

  // ==================================================
  // SERVO
  // ==================================================
  servoMotor.attach(pinoServo);

  // Posição inicial: cofre fechado
  servoMotor.write(90);

  // ==================================================
  // LCD
  // ==================================================
  lcd.begin(16, 2);

  lcd.setCursor(0, 0);
  lcd.print("Cofre Digital");

  lcd.setCursor(0, 1);
  lcd.print("Inicializando");

  delay(1000);

  lcd.clear();

  isIAAtivada = false;
}

// ==================================================
// LOOP PRINCIPAL
// ==================================================
void loop()
{
  // ==================================================
  // LEITURA DA IA
  // ==================================================
  lerIA();

  // ==================================================
  // LEITURA DO POTENCIÔMETRO
  // ==================================================
  int valor = analogRead(pinoPotencia);

  lcd.display();

  // ==================================================
  // BLOQUEIO
  // ==================================================
  if (bloqueado)
  {
    tone(buzzer, 800, 500);

    delay(200);

    tone(buzzer, 1000, 500);

    delay(200);

    lcd.setCursor(0, 0);
    lcd.print("ALARME ATIVO    ");

    lcd.setCursor(0, 1);
    lcd.print("Cofre Travado   ");

    digitalWrite(pinoLedVermelho, HIGH);

    delay(300);

    digitalWrite(pinoLedVermelho, LOW);

    delay(300);

    // Verifica se o tempo de bloqueio acabou
    if (millis() - inicioBloqueio >= duracaoBloqueio)
    {
      noTone(buzzer);

      bloqueado = false;

      tentativas = 0;

      lcd.clear();
    }

    return;
  }

  // ==================================================
  // TIMEOUT
  // ==================================================
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

  // ==================================================
  // IA CONECTADA E ROSTO BLOQUEADO
  // ==================================================
  if (isIAAtivada && !iaLiberou)
  {
    etapaAtual = 0;

    if (!mensagemIAExibida)
    {
      lcd.clear();

      lcd.setCursor(0, 0);
      lcd.print("Rosto Obstruido");

      lcd.setCursor(0, 1);
      lcd.print("Cofre Bloqueado");

      mensagemIAExibida = true;
    }

    // Impede qualquer operação do cofre
    return;
  }

  // ==================================================
  // SE CHEGOU AQUI, PODE USAR NORMALMENTE
  // ==================================================
  mensagemIAExibida = false;

  cofre(valor);
}