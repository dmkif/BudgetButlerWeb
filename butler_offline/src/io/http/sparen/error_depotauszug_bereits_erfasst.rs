use crate::budgetbutler::view::request_handler::{handle_render_display_view, no_page_middleware};
use crate::io::html::views::sparen::error_depotauszug_bereits_erfasst::render_error_depotauszug_bereits_erfasst_template;
use crate::model::state::config::ConfigurationData;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};

#[get("/error-depotauszug-bereits-erfasst")]
pub async fn error_depotauszug_bereits_erfasst(
    configuration: Data<ConfigurationData>,
) -> impl Responder {
    HttpResponse::Ok().body(handle_render_display_view(
        "Error Depotauszug bereits erfasst",
        "/",
        None,
        no_page_middleware,
        render_error_depotauszug_bereits_erfasst_template,
        configuration
            .configuration
            .lock()
            .unwrap()
            .database_configuration
            .name
            .clone(),
    ))
}
