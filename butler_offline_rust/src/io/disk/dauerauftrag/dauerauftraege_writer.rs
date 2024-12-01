use crate::io::disk::dauerauftrag::dauerauftrag_writer::write_dauerauftrag;
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::state::persistent_application_state::Database;

pub fn write_dauerauftraege(database: &Database) -> Vec<Line> {
    database.dauerauftraege.dauerauftraege.iter().map(|l| write_dauerauftrag(&l.value)).collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::dauerauftrag::Dauerauftrag;
    use crate::model::primitives::betrag::{betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::primitives::rhythmus::Rhythmus;
    use crate::model::state::persistent_application_state::builder::{dauerauftrage, empty_database_version, leere_einzelbuchungen, leere_gemeinsame_buchungen};

    #[test]
    fn test_write_dauerauftrag() {
        let dauerauftrag = Dauerauftrag {
            start_datum: Datum::new(1, 1, 2024),
            ende_datum: Datum::new(1, 1, 2025),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: betrag(Vorzeichen::Negativ, 123, 12),
            rhythmus: Rhythmus::Monatlich
        };
        let database = Database {
            einzelbuchungen: leere_einzelbuchungen(),
            db_version: empty_database_version(),
            dauerauftraege: dauerauftrage(dauerauftrag),
            gemeinsame_buchungen: leere_gemeinsame_buchungen(),
        };

        let lines = write_dauerauftraege(&database);

        assert_eq!(lines.len(), 1);
        assert_eq!(lines[0].line, "2024-01-01,2025-01-01,NeueKategorie,Normal,monatlich,-123.12");
    }

}