import Button from 'react-bootstrap/Button';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';


export default function OverlayButton({tip, handleButtonClick, buttonContent}) {
    return (
        <OverlayTrigger
            placement="bottom"
            overlay={<Tooltip id="button-tooltip-2" placement={"bottom"}>{tip}</Tooltip>}
        >
            {({ ref, ...triggerHandler }) => (
            <Button
                variant="light"
                {...triggerHandler}
                className="sm"
                onClick={handleButtonClick}
                ref={ref}
            >
                {buttonContent}
            </Button>
            )}
        </OverlayTrigger>
    )

}