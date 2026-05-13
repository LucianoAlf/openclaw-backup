from pathlib import Path
p=Path('/root/.openclaw/workspace/render_stage_attitude_carousel.py')
s=p.read_text()
repls={
".logo{position:absolute;top:48px;":".logo{position:absolute;top:56px;",
".logo img{height:76px;":".logo img{height:82px;",
".logo.lightlogo img{height:76px}":".logo.lightlogo img{height:82px}",
"font-size:34px;line-height:1.18":"font-size:39px;line-height:1.14",
"font-size:24px;line-height:1.16":"font-size:28px;line-height:1.14",
"font-size:24px;line-height:1.3":"font-size:30px;line-height:1.22",
"-webkit-text-stroke:2.8px #fff":"-webkit-text-stroke:3.4px #fff",
"-webkit-text-stroke:2.8px #0A0A0A":"-webkit-text-stroke:3.4px #0A0A0A",
"background:var(--pink);padding:28px;border-radius:26px;box-shadow:12px 12px 0 #000;transform:rotate(2deg)":"background:rgba(10,10,10,.86);padding:30px;border-radius:26px;box-shadow:12px 12px 0 rgba(233,20,81,.42);border:3px solid rgba(233,20,81,.9);transform:rotate(1.2deg)",
"<p>Movimento sem intenção vira distração.</p>":"<p>Sem intenção, movimento vira distração. Com intenção, vira presença.</p>",
"O palco lê seu corpo antes de ouvir sua voz.":"O palco lê seu corpo antes da voz sair.",
"Escolha 3 pontos no espaço: esquerda, centro e direita. Cante para pessoas, não para o medo.":"Escolha esquerda, centro e direita. Cante para pessoas, não para o medo.",
"Pausa não é vazio. Pausa é controle. Quem domina o silêncio domina a entrada.":"Pausa não é vazio. É controle. Quem domina o silêncio domina a entrada.",
"Atitude de palco não é parecer perfeito. É continuar presente quando algo sai do roteiro.":"Atitude não é parecer perfeito. É continuar presente quando algo sai do roteiro.",
"Vem cantar com presença, técnica e coragem. Sobe no palco com a LA Music School.":"Vem cantar com presença, técnica e coragem. Sobe no palco com a LA."
}
for a,b in repls.items(): s=s.replace(a,b)
p.write_text(s)
