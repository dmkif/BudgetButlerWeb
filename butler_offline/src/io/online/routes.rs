use crate::model::remote::server::ServerConfiguration;

pub fn offline_login_route(server_configuration: &ServerConfiguration) -> String {
    format!("{}/offlinelogin", server_configuration.server_url)
}

pub fn einzelbuchungen_route(server_configuration: &ServerConfiguration) -> String {
    format!("{}/api/einzelbuchungen", server_configuration.server_url)
}

pub fn kategorien_route(server_configuration: &ServerConfiguration) -> String {
    format!("{}/api/kategorien", server_configuration.server_url)
}

pub fn kategorien_batch_route(server_configuration: &ServerConfiguration) -> String {
    format!("{}/api/kategorien/batch", server_configuration.server_url)
}

pub fn gemeinsame_buchungen_batch_route(server_configuration: &ServerConfiguration) -> String {
    format!(
        "{}/api/gemeinsame_buchung/batch",
        server_configuration.server_url
    )
}

pub fn gemeinsame_buchungen_route(server_configuration: &ServerConfiguration) -> String {
    format!(
        "{}/api/gemeinsame_buchungen",
        server_configuration.server_url
    )
}
