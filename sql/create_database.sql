create table realestates (
	id serial primary key,
    naziv_oglasa varchar(255),
    tip_nekretnine varchar(50),
    kvadratura_m2 int,
    lokacija_naselje varchar(150),
    lokacija_grad varchar(150),
    cijena_km int,
    broj_soba int,
	broj_spavacih_soba int,
	droj_kupatila int,
	broj_toaleta int,
	sprat int,
	površina_nekretnine int,
	ukupna_površina_parcele int,
    površina_dvorišta int,
	godina_izgradnje int,
	godina_posljednje_adaptacije int,
	ukupan_broj_stambenih_jedinica int,
	ukupan_broj_spratova int,
	plin int,
	voda int,
	električna_energija int,
	kanalizacija int,
	telefonski_priključak int,
	interfon int,
	kablovska_tv int,
	internet int,
	ostava int
)